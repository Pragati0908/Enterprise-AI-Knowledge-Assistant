# Week 11 – Warning Review

## Project
**Enterprise AI Knowledge Assistant**

## Purpose
This document records the warning review and cleanup completed during Week 13. The objective was to identify, investigate, and resolve deprecation and compatibility warnings reported by the automated test suite without making unnecessary dependency changes.

---

## 1. Warning Review Summary

The project initially reported warnings in three main areas:

1. Pydantic class-based configuration
2. `datetime.utcnow()` deprecation
3. Starlette/httpx TestClient compatibility

All identified warnings were reviewed and resolved.

### Final status

| Warning area | Status | Action |
|---|---|---|
| Pydantic class-based Config in authentication schema | Resolved | Migrated to Pydantic v2 `ConfigDict` / `model_config` |
| Pydantic class-based Config in application settings | Resolved | Migrated settings configuration to the Pydantic v2-compatible form |
| `datetime.utcnow()` deprecation | Resolved | Updated the affected datetime handling after checking the application's database/timezone expectations |
| Starlette/httpx TestClient deprecation | Resolved | Updated the TestClient dependency/compatibility configuration so the deprecated combination is no longer used |

---

## 2. Pydantic Configuration Cleanup

The authentication response schema originally used the Pydantic v1-style:

```python
class Config:
    from_attributes = True
```

This was migrated to the Pydantic v2-compatible configuration:

```python
model_config = ConfigDict(
    from_attributes=True
)
```

The application settings configuration was also updated to remove the remaining class-based Pydantic configuration warning.

### Verification

The authentication schemas imported successfully after the change:

```text
Authentication schemas imported successfully
```

The focused authentication/security regression tests also passed successfully.

---

## 3. Datetime Deprecation Cleanup

The test suite had reported a Python deprecation warning associated with:

```python
datetime.utcnow()
```

The affected implementation was reviewed before changing the datetime representation. The replacement was made consistently with the application's UTC/database expectations rather than applying a blind global replacement.

This removed the deprecated `datetime.utcnow()` usage from the tested application path.

---

## 4. Starlette/httpx Warning Cleanup

The test suite had initially reported:

```text
StarletteDeprecationWarning:
Using `httpx` with `starlette.testclient` is deprecated
```

The dependency/compatibility issue was reviewed and corrected without making unrelated package changes.

The final regression run completed without the earlier warning output.

---

## 5. Final Verification

The final full regression command was:

```powershell
pytest -v
```

Result:

```text
41 passed in 68.83s (0:01:08)
```

No warnings summary was reported in the final run.

This confirms that the warning cleanup did not break the existing automated test suite.

---

## 6. Conclusion

The Week 11 warning cleanup is complete.

The project no longer reports the previously identified Pydantic, datetime, or Starlette/httpx deprecation warnings during the final regression run.

The changes were intentionally limited to compatibility and maintenance improvements. No unnecessary dependency reinstallation or broad architectural changes were required.

**Status: COMPLETE**
