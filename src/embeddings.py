from langchain.embeddings import HuggingFaceEmbeddings


MODEL_ID = "BAAI/bge-large-zh-v1.5"

# Create a dictionary with model configuration options, specifying to use the CPU for computations
model_kwargs = {'device':'cuda'}

# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': True}

# Initialize an instance of HuggingFaceEmbeddings with the specified parameters
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_ID,     # Provide the pre-trained model's path
    model_kwargs=model_kwargs, # Pass the model configuration options
    encode_kwargs=encode_kwargs # Pass the encoding options
)
