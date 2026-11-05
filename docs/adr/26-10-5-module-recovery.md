# Module retrieval

**Context:** We need to change how we retrieve modules from tags and I/O.
**Decision:** Use a hash and a name to avoid confusion when obtaining a module.
**Reasons:** By using a specific name and a hash, we can now ensure we get a specific module.

# Module Usage

**Context:** For now modules are not used due to qall implementation. 
**Decision:** Use static implementation as a placeholder
**Reasons:** Qall doesn't fully support imports making modules unusable
