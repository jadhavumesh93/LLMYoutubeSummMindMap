from Services.YoutubeService import YoutubeService
from Services.LLMEmbeddings import LLMEmbeddings
from Services.RAGService import RAGService

class EntryPoint:
    def __init__(self):
        pass
    
    def process(self, video_url = None, question = None):
        # 1.A. Check if URL is specified
        if(video_url == None or video_url == ""):
            return ("error", "Please enter Video URL")
        print("1.A Success")
        # 1.B. Check if Question is specified
        if(question == None or question == ""):
            return ("error", "Please enter Question")
        print("1.B Success")
        # 2. Get Transcript for the Video
        yt_service = YoutubeService(video_url)
        (status, video_valid) = yt_service.check_valid_url()
        if(status == "error"):
            return (status, video_valid)
        print("2.A Success")
        (status, video_id) = yt_service.extract_video_id()
        if(status == "error"):
            return (status, video_id)
        print("2.B Success")
        '''(status, video_title) = yt_service.extract_video_title(video_url)
        if(status == "error"):
            return (status, video_title)
        '''
        (status, transcript) = yt_service.process()
        if(status == "error"):
            return (status, transcript)
        print("2.C Success")
        
        # 3. Generate/Get Embeddings
        video_title = "Youtube Video"
        llm_emb = LLMEmbeddings(video_url=video_url, video_id=video_id, video_title=video_title, text=transcript)
        (status, llm_res) = llm_emb.process()
        if(status == "error"):
            return (status, llm_res)
        print("3 Success")
        
        # 4. Query RAG service
        rag_ser = RAGService(llm_res)
        (status, response) = rag_ser.generator(question=question)
        print("4 Success")
        return (status, response)
'''
# For New Video

# 1. Specify Youtube Video
video_url = "https://www.youtube.com/watch?v=P3oi1vYRq9c"

# 2. Get Transcript for the Video
yt_service = YoutubeService()
(status, video_id) = yt_service.extract_video_id(video_url)
(status, video_title) = yt_service.extract_video_title(video_url)
(status, transcript) = yt_service.process(video_url)

# 3. Generate/Get Embeddings
llm_emb = LLMEmbeddings(video_url=video_url, video_id=video_id, video_title=video_title, text=transcript)
(status, llm_res) = llm_emb.process()

# 4. Query RAG service
rag_ser = RAGService(llm_res)
(status, response) = rag_ser.generator(question="Is traditional ML dead?")

#print(response)


# 2. For Existing videos
# 3. Generate/Get Embeddings
llm_emb = LLMEmbeddings(new_video = False)
(status, llm_res) = llm_emb.process()

# 4. Query RAG service
rag_ser = RAGService(llm_res)
(status, response) = rag_ser.generator(question="What is ecosystem?")
'''