import streamlit as st
from utils.searcher import research_topic
from utils.summarizer import summarise_sources_to_bullets
from utils.writer import write_linkedin_post


st.set_page_config(page_title="AI LinkedIn Post Generator", layout="wide")

st.title("🤖 AI LinkedIn Post Generator")

with st.sidebar:
    st.header("Settings")
    num_results = st.number_input("Search results (SerpAPI)", min_value=3, max_value=10, value=6)
    fetch_limit = st.number_input("Pages to fetch & scrape", min_value=1, max_value=5, value=3)
    tone = st.selectbox("Tone", ["professional", "friendly", "inspirational"], index=0)
    length = st.selectbox("Post length", ["short", "medium", "long"], index=1)
    show_sources = st.checkbox("Show full scraped sources", value=True)

topic = st.text_input("Enter topic (e.g. 'concepts of machine learning')", value="", max_chars=200)

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Generate Post"):
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Running research and generating post..."):
                # Research
                sources = research_topic(topic, num_results=int(num_results), fetch_limit=int(fetch_limit))
                st.session_state["sources"] = sources

                # Summarize
                research_summary = summarise_sources_to_bullets(sources)
                st.session_state["research_summary"] = research_summary

                # Write post
                post = write_linkedin_post(research_summary, tone=tone, length=length)
                st.session_state["post"] = post

    # Show results area
    if "research_summary" in st.session_state:
        st.subheader("🔍 Research Summary")
        st.markdown(st.session_state["research_summary"])

    if "post" in st.session_state:
        st.subheader("✍️ Generated LinkedIn Post")
        post_text = st.text_area("Edit the post before approving:", value=st.session_state["post"], height=220)
        st.session_state["post"] = post_text

        row_col1, row_col2, row_col3 = st.columns([1,1,1])
        with row_col1:
            if st.button("Regenerate Post (same summary)"):
                with st.spinner("Regenerating post..."):
                    st.session_state["post"] = write_linkedin_post(st.session_state["research_summary"], tone=tone, length=length)
                    st.rerun()

        with row_col2:
            if st.button("Regenerate Research (redo search)"):
                with st.spinner("Re-running research..."):
                    sources = research_topic(topic, num_results=int(num_results), fetch_limit=int(fetch_limit))
                    st.session_state["sources"] = sources
                    st.session_state["research_summary"] = summarise_sources_to_bullets(sources)
                    st.session_state["post"] = write_linkedin_post(st.session_state["research_summary"], tone=tone, length=length)
                    st.experimental_rerun()

        with row_col3:
            if st.button("Approve (final)"):
                st.success("Post approved. You can copy it or publish via LinkedIn integration.")
                # Save approved post somewhere or call publish function (if integrated)
                st.session_state["approved_post"] = st.session_state["post"]

with col2:
    st.markdown("### Sources")
    if "sources" in st.session_state:
        for i, s in enumerate(st.session_state["sources"], start=1):
            st.markdown(f"**{i}. [{s.get('title')}]({s.get('url')})**")
            st.write(s.get("snippet") or "")
            if show_sources:
                if s.get("content"):
                    st.expander("Show scraped content", expanded=False).write(s.get("content")[:2000] + ("..." if len(s.get("content")) > 2000 else ""))
    else:
        st.info("Search results will show up here after you click 'Generate Post'.")

st.markdown("---")
st.markdown("Built with :heart: — modify modules in `utils/` to improve search provider, LLM model, or add LinkedIn publishing.")
