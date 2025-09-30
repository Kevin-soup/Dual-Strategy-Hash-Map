# Dual-Strategy Hash Map — Separate Chaining & Quadratic Probing

A production-style **hash map data structure** implemented in two interchangeable styles:
- **Separate Chaining** (array of buckets, each bucket is a lightweight linked list)
- **Open Addressing with Quadratic Probing** (single array; collisions resolved by a quadratic probe sequence)

Both variants share the same interface behind the scenes and can be swapped based on workload or memory needs.

---

## Implementations

### Separate Chaining
- **Structure:** An array of buckets; each bucket holds a small linked list of `(key, value)` nodes.
- **Collisions:** Multiple colliding keys are kept as distinct nodes in the same bucket.
- **Pros:** Simple to reason about, tolerant of higher load factors, straightforward deletions.
- **Cons:** Extra pointers per node (slightly higher memory overhead); cache locality is less favorable than array-only designs.

### Open Addressing (Quadratic Probing)
- **Structure:** A single array of entries; empty slots and *tombstones* (deleted markers) manage occupancy.
- **Collisions:** Resolve by probing indices using a quadratic sequence until a free or matching slot is found.
- **Pros:** Excellent cache locality, minimal per-entry overhead.
- **Cons:** Deletions require tombstones to maintain probe chains; sensitive to load factor and capacity choice.

---

## Core Data-Structure Concepts

### Hashing & Indexing
- Uses the language runtime’s `hash(key)` (or a pluggable hash) normalized into `[0, capacity)`.
- Good hash distribution reduces clustering and keeps probe lengths/bucket sizes modest.

### Load Factor & Resizing
- **Load factor** (`entries / capacity`) is tracked to determine when to grow the table.
- When a threshold is exceeded (e.g., `0.7`), the table **resizes** and all entries are redistributed (rehashed).

### Memory & Ordering
- Separate Chaining allocates small nodes per entry; Open Addressing keeps entries inline.
- Iteration order is implementation-defined and not guaranteed to be stable between resizes.

### Correctness Invariants
- Exactly one stored entry per distinct key; resizing preserves all key–value pairs.
- Key hashing and equality must be consistent across the map’s lifecycle.

---

## Testing Approach
- Unit tests for insert/update/delete/lookup; forced collisions and resize scenarios.  
- Differential checks against a reference map on randomized workloads.

---

## Notes 
- Keys must be hashable with consistent equality; iteration order is unspecified.  
- Open addressing uses tombstones on delete; chaining stores colliding keys in per-bucket lists.
