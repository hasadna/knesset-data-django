import re, logging
from xml.etree import ElementTree
from knesset_data_django.mks.utils import get_all_mk_names
from .models import ProtocolPart, CommitteeMeeting

logger = logging.getLogger(__name__)
speaker_text_threshold = 40

_parts = None
_mks_attended = set()
_mks = None
_mk_names = None


def _plenum_parse_para_element(para):
    is_bold = False
    if para.find('emphasis') is not None:
        is_bold = True
    txt = ''
    for subtext in para.itertext():
        txt += subtext
    return is_bold, txt


def _plenum_parse_para_text(para, is_bold):
    t = 'text'
    if is_bold and re.search(r":[\s]*$", para) is not None:
        # bold + ends with a colon
        t = 'speaker'
    elif is_bold:
        t = 'title'
    return t


def _plenum_parse_para(txt, t, titles):
    if titles is None:
        titles = []
        if t == 'speaker':
            titles.append({u't': u'', u'c': [
                {u't': txt, u'c': [], u's': 1}
            ]})
        elif t == 'title':
            titles.append({u't': txt, u'c': []})
        else:
            titles.append({u't': '', u'c': [
                {u't': txt, u's': 0}
            ]})
    elif t == 'title':
        titles.append({u't': txt, u'c': []})
    else:
        title = titles[len(titles) - 1]
        children = title['c']
        if t == 'speaker':
            children.append({u't': txt, u'c': [], u's': 1})
        elif len(children) == 0:
            children.append({u't': txt, u's': 0})
        elif children[len(children) - 1]['s'] == 1:
            children[len(children) - 1]['c'].append({u't': txt})
        else:
            children.append({u't': txt, u's': 0})
    return titles


def _save_part(meeting, header, body, type):
    global _partsCounter
    global _parts
    _parts.append(
        ProtocolPart(meeting=meeting, order=len(_parts), header=header.strip(), body=body.strip(), type=type)
    )
    if type == 'speaker' and len(body.strip()) > speaker_text_threshold:
        for (i, name) in enumerate(_mk_names):
            if header.find(name) > -1:
                _mks_attended.add(_mks[i])


def create_plenum_protocol_parts(meeting, mks=None, mk_names=None):
    global _mks
    global _mk_names
    if mks is None or mk_names is None:
        (mks, mk_names) = get_all_mk_names()
    (_mks, _mk_names) = (mks, mk_names)
    global _parts
    _parts = []
    txt = meeting.protocol_text.encode('utf-8')
    tree = ElementTree.fromstring(txt)
    titles = None
    for para in tree.iter('para'):
        (isBold, txt) = _plenum_parse_para_element(para)
        t = _plenum_parse_para_text(txt, isBold)
        titles = _plenum_parse_para(txt, t, titles)
    for title in titles:
        title_header = title['t'].strip()
        title_body = []
        # _savePart(meeting,'',t,'title')
        for child in title['c']:
            if child['s'] == 1:
                # it's a speaker, save the aggregated title texts
                if len(title_header) > 0 or len(title_body) > 0:
                    _save_part(meeting, title_header, '\n\n'.join(title_body), 'title')
                    title_header = ''
                    title_body = []
                speaker_header = child['t'].strip()
                speaker_text = []
                for schild in child['c']:
                    t = schild['t'].strip()
                    if len(t) > 0:
                        speaker_text.append(t)
                _save_part(meeting, speaker_header, '\n\n'.join(speaker_text), 'speaker')
            else:
                t = child['t'].strip()
                if len(t) > 0:
                    title_body.append(t)
        if len(title_header) > 0 or len(title_body) > 0:
            _save_part(meeting, title_header, '\n\n'.join(title_body), 'title')
    if len(_parts) > 0:
        # find duplicates
        got_duplicate = False
        other_meetings = CommitteeMeeting.objects.filter(date_string=meeting.date_string).exclude(id=meeting.id)
        if len(other_meetings) > 0:
            for other_meeting in other_meetings:
                if other_meeting.parts.count() == len(_parts):
                    meeting.delete()
                    got_duplicate = True
        if got_duplicate:
            logger.debug('got a duplicate meeting - deleting my meeting')
        else:
            ProtocolPart.objects.bulk_create(_parts)
            logger.debug('wrote ' + str(len(_parts)) + ' protocol parts')
            for mk in _mks_attended:
                meeting.mks_attended.add(mk)
