import os
import re
import yaml

# Structure to represent our document chunks
class DocChunk:
    def __init__(self, document_id: str, title: str, status: str, audience: str, 
                 policy_authority: str, file_name: str, heading: str, content: str):
        self.document_id = document_id
        self.title = title
        self.status = status
        self.audience = audience
        self.policy_authority = policy_authority
        self.file_name = file_name
        self.heading = heading
        self.content = content
        self.full_source = f"{file_name} > {heading}"

    def to_dict(self):
        return {
            "document_id": self.document_id,
            "title": self.title,
            "status": self.status,
            "audience": self.audience,
            "policy_authority": self.policy_authority,
            "file_name": self.file_name,
            "heading": self.heading,
            "content": self.content,
            "full_source": self.full_source
        }

def parse_markdown_file(file_path: str):
    """
    Extracts the YAML front-matter and the body of a markdown file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Match the front-matter delimited by ---
    match = re.match(r"^---\r?\n([\s\S]+?)\r?\n---\r?\n([\s\S]*)$", file_content)
    if not match:
        return {}, file_content

    yaml_content = match.group(1)
    body_content = match.group(2) or ""

    try:
        metadata = yaml.safe_load(yaml_content) or {}
        return metadata, body_content
    except Exception as e:
        print(f"Error parsing YAML in {file_path}: {e}")
        return {}, body_content

def ingest_knowledge_base(kb_dir: str):
    """
    Reads all markdown files in the knowledge base and splits them into section chunks.
    """
    chunks = []
    if not os.path.exists(kb_dir):
        print(f"Error: knowledge base directory '{kb_dir}' not found.")
        return chunks

    files = [f for f in os.listdir(kb_dir) if f.endswith('.md')]

    for file in files:
        file_path = os.path.join(kb_dir, file)
        metadata, content = parse_markdown_file(file_path)

        doc_id = metadata.get("document_id", file)
        title = metadata.get("title", file)
        status = metadata.get("status", "unknown")
        audience = metadata.get("audience", "unknown")
        policy_authority = metadata.get("policy_authority", "none")

        # Split the document by subheadings (e.g. "## Standard return window")
        # We use re.split with lookahead so the headings are preserved in the list
        sections = re.split(r"(?=^##\s+)", content, flags=re.MULTILINE)

        current_heading = "Introduction"

        for section in sections:
            trimmed = section.strip()
            if not trimmed:
                continue

            section_content = trimmed
            heading = current_heading

            # Check if this section starts with a header line
            heading_match = re.match(r"^##\s+(.+)$", trimmed, flags=re.MULTILINE)
            if heading_match:
                heading = heading_match.group(1).strip()
                # Remove the header line to keep only the paragraph body text
                section_content = re.sub(r"^##\s+.+$", "", trimmed, count=1, flags=re.MULTILINE).strip()

            chunks.append(DocChunk(
                document_id=doc_id,
                title=title,
                status=status,
                audience=audience,
                policy_authority=policy_authority,
                file_name=file,
                heading=heading,
                content=section_content
            ))

    return chunks
