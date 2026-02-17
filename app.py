import socket
print(socket.gethostbyname("google.com"), flush=True)
print(socket.gethostbyname("huggingface.co"), flush=True)
print(socket.gethostbyname("www.youtube.com"), flush=True)


import streamlit as st
from EntryPoint import EntryPoint

st.title('Retrieval-Augmented Video Knowledge Engine')
st.write("Note: - Since the developer is keen on reducing infrastructure costs, the next time you access this space, you may not receive desired response. Since the HuggingFace space is based on serverless architecture, the storage is non-persistent. Hence any video that you upload may not be acquired by the system for long time.")
st.write("However, once you access the space, you may work with numerous Youtube videos while querying for the previous videos questions as well. P.S. Due to the limitations of the Space, a valid URL will always be required (does not matter if you ask questions for the previous any video that you worked upon) or You may get URL required error.")

video_url = st.text_input("Enter Youtube video URL", placeholder="Example - https://www.youtube.com/watch?v=RNF0FvRjGZk")
question = st.text_input("Enter your question for the video", placeholder="Example - What is the video about?")

if(st.button("Submit")):
    if(video_url == None or video_url == ""):
        #st.write("Please Enter Video URL")
        st.write(
            f"<p style='color : red'>Please Enter Video URL</p>",
            unsafe_allow_html=True
        )
    if(question == None or question == ""):
        st.write(
            f"<p style='color : red'>Please Enter Question</p>",
            unsafe_allow_html=True
        )
    if(video_url and question):
        entrypoint = EntryPoint()
        (status, response) = entrypoint.process(video_url=video_url, question=question)
        if(status != "success"):
            st.write(
                f"<p style='color : red'>{response}</p>",
                unsafe_allow_html=True
            )
        else:
            st.write(
                f"<h3 style='text-align : centre'>Here is Your Response</h3>",
                unsafe_allow_html=True
            )
            st.write(
                f"<p>{response}</p>",
                unsafe_allow_html=True
            )
            
st.write(
    "<i>Prototype by <u>Umesh Jadhav</u></i> <a style='margin-left : 1%' href='https://github.com/jadhavumesh93/LLMYoutubeSummMindMap.git' target='_blank'>Github</a>",
    unsafe_allow_html=True
)