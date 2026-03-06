# AgentOS Knowledge API Reference

## Complete Knowledge Endpoints

### GET /knowledge/config
Get knowledge base configuration including available readers and chunkers.

### GET /knowledge/content
List all content with pagination and sorting.

**Query Parameters:**
- `limit` (integer, default: 20): Items per page
- `page` (integer, default: 1): Page number
- `sort_by` (string, default: `created_at`): Sort field
- `sort_order` (string, default: `desc`): Sort direction
- `db_id` (string): Database ID
- `knowledge_id` (string): Knowledge base ID

**Response:** `PaginatedResponse` with content objects:
- `id`, `name`, `description`, `type`, `size`, `metadata`
- `access_count`, `status`, `status_message`
- `created_at`, `updated_at`

### GET /knowledge/content/{content_id}
Get specific content by ID.

### GET /knowledge/content/{content_id}/status
Get processing status of a content item.

**Response:** Status object with `status` and `status_message`.

### POST /knowledge/search
Search the knowledge base.

**Body Parameters:**
- `query` (string): Search query
- `limit` (integer): Max results

**Response:** Array of search results with `content` and `score`.

### POST /knowledge/content
Upload content to the knowledge base. Supports file uploads, text content, or URLs. Content is processed asynchronously.

**Body Parameters:**
- `text_content` (string): Raw text to upload
- `name` (string): Content name
- `description` (string): Content description

### PATCH /knowledge/content/{content_id}
Update content metadata (name, description) without re-uploading.

### DELETE /knowledge/content
Delete all content in the knowledge base.

### DELETE /knowledge/content/{content_id}
Delete specific content by ID.

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# Config
config = await client.get_knowledge_config()

# Upload
result = await client.upload_knowledge_content(
    text_content="Content to upload",
    name="Content Name",
    description="Description",
)
# result.id, result.status

# Status
status = await client.get_content_status(content_id)
# status.status, status.status_message

# Search
results = await client.search_knowledge(query="search terms", limit=5)
# results.data — list with content and score

# List
content = await client.list_knowledge_content()
# content.data — list of content objects

# Delete
await client.delete_content(content_id)
await client.delete_all_content()
```

## Content Processing States

Content is processed asynchronously after upload:
- `pending` — Queued for processing
- `processing` — Currently being processed
- `completed` — Successfully processed and searchable
- `failed` — Processing failed (check `status_message`)
