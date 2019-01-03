A prototype wrapper around Azure search for Python

For this to work you need the following environment variables set:

    AZURE_SEARCH_API_KEY={a regular search api key}
    AZURE_SEARCH_ADMIN_API_KEY={a search admin api key}
    AZURE_SEARCH_URL=https://{your search service name}.search.windows.net

Features:
1. Define fields and indexes through Python
2. Deine skills and skillsets: Predefined Cognitive Search skills and custom skills (WebAPI skills)
3. Define analyzers (custom analyzers and predefined analyzers)
4. Define scoring profiles, suggesters
5. Upload documents to Azure Search 
