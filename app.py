from Services.YoutubeService import YoutubeService
from Services.LLMEmbeddings import LLMEmbeddings
from Services.RAGService import RAGService

# For New Video
'''
# 1. Specify Youtube Video
video_url = "https://www.youtube.com/watch?v=RNF0FvRjGZk"

# 2. Get Transcript for the Video
yt_service = YoutubeService()
(status, video_id) = yt_service.extract_video_id(video_url)
(status, transcript) = yt_service.process(video_url)

# 3. Generate/Get Embeddings
llm_emb = LLMEmbeddings(video_url=video_url, video_id=video_id, text=transcript, new_video = True)
(status, llm_res) = llm_emb.process()

# 4. Query RAG service
rag_ser = RAGService(llm_res)
(status, response) = rag_ser.generator(question="Explain me the concept in the video.")

#print(response)
'''

# 2. For Existing videos
# 3. Generate/Get Embeddings
llm_emb = LLMEmbeddings(new_video = False)
(status, llm_res) = llm_emb.process()

# 4. Query RAG service
rag_ser = RAGService(llm_res)
(status, response) = rag_ser.generator(question="Explaine me attention in simple way.")
