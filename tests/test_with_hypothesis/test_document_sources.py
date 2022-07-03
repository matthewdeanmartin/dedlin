from collections import ChainMap

from hypothesis import given
from hypothesis import strategies as st

import dedlin.document_sources


@given(
    lines=st.one_of(
        st.lists(st.text()),
        st.sets(st.text()),
        st.frozensets(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()),
        st.dictionaries(keys=st.text(), values=st.none()).map(dict.keys),
        st.dictionaries(keys=st.integers(), values=st.text()).map(dict.values),
        st.iterables(st.text()),
        st.dictionaries(keys=st.text(), values=st.text()).map(ChainMap),
    )
)
def test_fuzz_InMemoryInputter(lines):
    dedlin.document_sources.InMemoryInputter(lines=lines)


# needs mock
# @given(prompt=st.text(), default=st.text())
# def test_fuzz_input_with_prefill(prompt, default):
#     dedlin.document_sources.input_with_prefill(prompt=prompt, default=default)
