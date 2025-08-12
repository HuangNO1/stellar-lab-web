<!-- Language Switcher -->

<div align="right">

[简体中文](delete_logc.md)

</div>

# Soft Delete Relational Constraints Implementation Summary

All soft delete relational constraints have now been implemented:

## 📋 Soft Delete Relational Constraints Summary

### ✅ Laboratory Deletion

- Check for valid research groups → Prevent deletion
- Check for valid members → Prevent deletion

### ✅ Research Group Deletion

- Check for valid members → Prevent deletion

### ✅ Member Deletion

- Check if member is research group leader → Prevent deletion
- Check for associated valid papers → Prevent deletion

### ✅ Member Batch Deletion

- Check if batch members include research group leaders → Prevent deletion
- Check if batch members have paper associations → Prevent deletion

## 🔗 Relational Hierarchy Structure

```bash
Laboratory Lab
├── Research Group ResearchGroup (mem_id → Leader)
│   └── Member Member
│       └── Paper Author PaperAuthor → Paper
└── Member Member (lab_id)
    └── Paper Author PaperAuthor → Paper
```

This ensures data integrity: users must handle relational dependencies in the order of Papers → Members → Research Groups → Laboratory to successfully delete higher-level records.