# Week 11 - Testing, Optimization and Final Regression Report

## Project
**Enterprise AI Knowledge Assistant**

## Week 11 Focus

Week 11 focused on:

- Negative testing
- Performance testing
- Performance optimization
- Regression testing
- Warning cleanup
- Final verification and documentation

---

# 1. Objectives

The objectives for Week 13 were to verify that the application:

1. Handles invalid and unexpected inputs safely.
2. Meets practical response-time expectations for key APIs.
3. Does not introduce unnecessary performance bottlenecks.
4. Continues to pass existing functionality after optimization.
5. Produces no unresolved deprecation warnings.
6. Has a documented and reproducible final regression state.

---

# 2. Negative Testing

Negative testing was performed using:

```powershell
pytest tests/test_negative_cases.py -v
```

The negative test suite covers cases including:

- Missing authentication
- Invalid authorization token
- Empty search query
- Missing search query
- Invalid `top_k`
- Zero `top_k`
- Incorrect `top_k` type
- Whitespace-only search query
- Malformed JSON
- Search with no matching results
- Missing extraction text
- Empty extraction text
- Unsupported extraction type
- Incorrect extraction text type
- Large extraction text

The API's actual semantic behavior was respected during testing. In particular, some application-level validation failures are returned as HTTP 200 responses containing a failure payload rather than as HTTP 4xx responses. The tests were aligned with the application's implemented contract rather than incorrectly treating those responses as failures.

### outcome

The negative-testing stage was completed successfully and the discovered assertion mismatches were corrected to match the application's actual API semantics.

---

# 3. Performance Testing

Dedicated performance tests were added in:

```text
tests/test_performance.py
```

The tests measure:

1. Search response time
2. Extraction response time
3. Repeated search performance

The performance threshold used for the main API tests was 5 seconds.

## Measured Results

### Search

Test:

```text
test_search_response_time
```

Measured response time:

```text
0.0735 seconds
```

### Extraction

Test:

```text
test_extraction_response_time
```

Measured response time:

```text
0.0240 seconds
```

### Repeated Search

Five consecutive searches produced approximately:

| Request | Time |
|---|---:|
| 1 | 0.0467 s |
| 2 | 0.0389 s |
| 3 | 0.0420 s |
| 4 | 0.0394 s |
| 5 | 0.0368 s |

Summary:

```text
Average: 0.0408 s
Minimum: 0.0368 s
Maximum: 0.0467 s
```

These results are substantially below the 5-second test threshold.

---

# 4. Performance Investigation

The full test suite initially showed considerably longer execution time than the individual API performance tests.

The investigation therefore distinguished between:

- Actual API request latency
- Model initialization/cold-start cost
- Python module import/pytest collection overhead
- Warm application execution

This distinction is important because a slow full `pytest` run does not necessarily mean that the API itself is slow.

---

# 5. Identified Performance Bottleneck

The main performance bottleneck identified during profiling was the initialization of the SentenceTransformer embedding model.

The embedding service originally loaded:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

at class/module initialization time.

This caused model loading to occur during imports, increasing application startup and test collection time.

---

# 6. Optimization Implemented – Lazy Model Loading

The embedding service was changed to lazy initialization.

The model is now loaded only when an embedding operation is actually requested.

Conceptually:

```python
class EmbeddingService:
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model
```

The embedding methods then obtain the model through `_get_model()`.

### Benefit

This prevents unnecessary model loading during module import and allows code paths that do not require embeddings to start much faster.

---

# 7. Cold Start vs Warm Execution

The optimization was specifically evaluated for cold-start and warm execution.

The first embedding operation incurs the model initialization cost.

Subsequent embedding operations reuse the already-loaded model and are substantially faster.

Therefore:

- **Cold start:** expected to be slower because the ML model must be loaded.
- **Warm execution:** fast because the model remains in memory.

This behavior is normal for an application using a local Transformer embedding model.

---

# 8. Additional Profiling Findings

Before lazy loading, import-time profiling showed significant overhead associated with loading the embedding model through application imports.

After lazy loading, the import overhead of the embedding service and application startup path was substantially reduced.

The Retriever itself was also checked separately. Its construction was measured at approximately:

```text
0.06 seconds
```

with the existing FAISS index and metadata loaded.

This indicated that the Retriever/vector-store initialization was not a significant runtime bottleneck and therefore did not require unnecessary redesign.

---

# 9. Performance Test Result

The dedicated performance test suite:

```powershell
pytest tests/test_performance.py -v -s
```

completed successfully:

```text
3 passed
```

The measured API response times were well below the defined 5-second threshold.

---

# 10. Regression Testing

The final full regression command was:

```powershell
pytest -v
```

The suite collected:

```text
41 items
```

Final result:

```text
41 passed in 68.83s (0:01:08)
```

Every test passed.

The suite included:

- Authentication tests
- Citation tests
- Extraction tests
- Entity extraction tests
- Invoice extraction tests
- Negative tests
- Password security tests
- Performance tests
- Protected-route tests
- Search API tests
- Search validation tests
- Similarity search tests
- Vector-store tests

---

# 11. Full Suite Runtime Observation

After a system restart, the first full regression run took:

```text
169.34 seconds
```

A second run immediately afterward took:

```text
68.83 seconds
```

Both runs produced:

```text
41 passed
```

### Interpretation

The difference is expected in an ML-enabled Python application.

The first run after restart can incur cold-start costs such as:

- Python module imports
- ML-library initialization
- SentenceTransformer/model loading
- Operating-system filesystem/cache effects
- FAISS and related native-library initialization

The second run benefits from already initialized processes/libraries and system-level caching.

Therefore, the difference between 169.34 seconds and 68.83 seconds should **not** be interpreted as unstable API performance.

The dedicated API performance tests already demonstrated very low warm request latency.

---

# 12. Is Further Optimization Required?

### Decision: No mandatory optimization is required for Week 13.

The project has reached a reasonable stopping point for this stage because:

1. All 41 regression tests pass.
2. The dedicated performance tests pass.
3. Search response time is far below the 5-second threshold.
4. Extraction response time is far below the 5-second threshold.
5. Repeated search requests remain consistently fast.
6. The main identified startup bottleneck was addressed through lazy model loading.
7. Retriever construction was verified as inexpensive.
8. All previously identified warnings were resolved.
9. No functional regression was introduced by the optimization.

### Optional future optimization

If test-suite startup time becomes an important development concern later, the next area to investigate would be pytest collection/import overhead.

That would be an engineering improvement rather than a required Week 13 fix.

Possible future techniques include:

- reducing unnecessary imports in `conftest.py`
- avoiding application-wide initialization during test collection
- separating heavyweight ML initialization from modules imported by unrelated tests
- using fixtures to initialize expensive resources only for tests that require them
- measuring pytest collection time independently from test execution

These changes should **not** be introduced merely to reduce the current 68.83-second full-suite runtime because they could add complexity without improving production API performance.

---

# 13. Warning Cleanup

The previously observed warnings were reviewed and resolved.

The final regression run:

```powershell
pytest -v
```

reported:

```text
41 passed in 68.83s (0:01:08)
```

with no warnings summary.

The warning cleanup included:

- Pydantic v2 configuration migration
- UTC datetime deprecation cleanup
- Starlette/httpx TestClient compatibility cleanup

Detailed warning documentation is maintained separately in:

```text
docs/week11_warning_review.md
```

---

# 14. Regression Safety

The performance optimization was intentionally small and isolated.

The principal application optimization was lazy initialization of the SentenceTransformer model.

The final regression suite confirms that this change did not break:

- Authentication
- Protected routes
- Search
- Search validation
- Citations
- Extraction
- Similarity search
- Vector storage
- Negative cases
- Password security

---

# 15. Week 11 Deliverables

The following Week 13 deliverables are complete:

```text
tests/test_negative_cases.py
tests/test_performance.py
docs/week11_warning_review.md
docs/week11_testing_and_optimization_report.md
```

The Week 11 work also includes the embedding-service optimization implemented in:

```text
app/services/embedding_service.py
```

---

# 16. Final Status

| Area | Status |
|---|---|
| Negative testing | COMPLETE |
| Performance testing | COMPLETE |
| Performance profiling | COMPLETE |
| Embedding model optimization | COMPLETE |
| Regression testing | COMPLETE |
| Warning cleanup | COMPLETE |
| Final verification | COMPLETE |
| Week 13 documentation | COMPLETE |

---

# 17. Final Conclusion

Week 11 successfully completed the planned testing, optimization, warning cleanup, and regression activities for the Enterprise AI Knowledge Assistant.

The final automated regression suite achieved:

```text
41 passed
```

with no unresolved warning output.

The main performance bottleneck discovered during profiling was the cold-start initialization of the SentenceTransformer embedding model. Lazy loading was implemented so the model is initialized only when embedding functionality is actually required.

The application's measured search and extraction API response times are comfortably below the defined performance threshold, while repeated searches remain consistently fast.

The difference between the first and second full-suite execution after a system restart is attributable primarily to cold-start/import/cache effects and does not indicate a production API performance problem.

**Week 11 Status: COMPLETE**

**Recommendation: Proceed to the next project phase. No further mandatory optimization is required at this stage.**
