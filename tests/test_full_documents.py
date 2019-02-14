from collections import namedtuple
import pytest
import six

ContentElement = namedtuple('ContentElement', ('parsed', 'expected', 'index'))


@pytest.mark.skip(reason="Integration test; use this to test full html documents")
@pytest.mark.parametrize('file_name', [
    'fandango_list',  # list of links
])
def test_documents_content_elements(file_name, get_html_fixture, get_json_data, test_html2ans):
    parsed_content_elements = test_html2ans.generate_ans(
        get_html_fixture('input/{}.html'.format(file_name)))
    expected_content_elements = get_json_data('expected_output/{}.json'.format(file_name))
    num_elements = len(expected_content_elements)

    assert len(parsed_content_elements) == num_elements

    for index in range(num_elements):
        # parsed results have keys that are not important to inspect, so ignore
        raw_parsed = parsed_content_elements[index]
        raw_expected = expected_content_elements[index]
        for k in six.iterkeys(raw_expected):
            assert raw_parsed[k] == raw_expected[k], 'Mismatch at {}, {}'.format(index, k)
