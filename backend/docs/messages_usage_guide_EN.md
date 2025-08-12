<!-- Language Switcher -->

<div align="right">

[简体中文](messages_usage_guide.md)

</div>

# Unified Text Management Usage Guide

## Overview

To solve the problem of hardcoded Chinese messages in the backend, we created a unified text management system. All Chinese messages returned to the frontend are centrally managed in the `app/utils/messages.py` file.

## File Structure

```
app/utils/
├── messages.py          # Unified text management file
└── ...
```

## Key Features

- **Centralized Management**: All Chinese messages are uniformly managed in the `Messages` class
- **Parameter Support**: Supports dynamic parameters such as `{count}`, `{field}`, etc.
- **Type Classification**: Success messages and error messages are managed separately
- **Simplified Calls**: Provides `msg` shortcut for concise usage
- **Easy Maintenance**: Facilitates future internationalization expansion

## Usage Methods

### 1. Usage in Service Layer

```python
from app.utils.messages import msg

# Basic error message
raise ValidationError(msg.get_error_message('MEMBER_NOT_FOUND'))

# Error message with parameters
raise ValidationError(msg.get_error_message('LAB_HAS_GROUPS', count=5))

# Convenient method for field length errors
raise ValidationError(msg.format_field_length_error('name', 100))

# Convenient method for file errors
raise ValidationError(msg.format_file_error('LOGO_UPLOAD_FAILED', error=str(e)))
```

### 2. Usage in Route Layer

```python
from app.utils.messages import msg

# Success message
return jsonify(success_response(data, msg.get_success_message('MEMBER_CREATE_SUCCESS')))

# Message-only response
return jsonify(success_response(message=msg.get_success_message('MEMBER_DELETE_SUCCESS')))
```

## Message Types

### Success Messages (SUCCESS)

- General operations: `CREATE_SUCCESS`, `UPDATE_SUCCESS`, `DELETE_SUCCESS`
- Login related: `LOGIN_SUCCESS`, `LOGOUT_SUCCESS`, `PASSWORD_CHANGE_SUCCESS`
- Specific modules: `LAB_UPDATE_SUCCESS`, `MEMBER_CREATE_SUCCESS`, etc.

### Error Messages (ERRORS)

- General errors: `NOT_FOUND`, `PERMISSION_DENIED`, `INVALID_INPUT`
- Authentication errors: `USER_NOT_FOUND`, `WRONG_PASSWORD`, `ACCOUNT_DISABLED`
- Business logic: `LAB_HAS_GROUPS`, `MEMBER_IS_GROUP_LEADER`
- Data validation: `EMAIL_FORMAT_INVALID`, `FIELD_LENGTH_EXCEEDED`

## Refactoring Progress

### ✅ Completed
- `app/services/lab_service.py`
- `app/routes/lab.py`
- `app/routes/root.py`
- `app/utils/file_handler.py`

### 📝 Files to be Refactored

**Service Layer Files:**
- `app/services/member_service.py`
- `app/services/paper_service.py`
- `app/services/news_service.py`
- `app/services/project_service.py`
- `app/services/research_group_service.py`
- `app/services/admin_service.py`
- `app/services/auth_service.py`
- `app/services/media_service.py`
- `app/services/base_service.py`

**Route Layer Files:**
- `app/routes/member.py`
- `app/routes/paper.py`
- `app/routes/news.py`
- `app/routes/project.py`
- `app/routes/research_group.py`
- `app/routes/admin.py`
- `app/routes/auth.py`
- `app/routes/media.py`

## Refactoring Steps

1. **Import Message Manager**
   ```python
   from app.utils.messages import msg
   ```

2. **Replace Hardcoded Messages**
   ```python
   # Original
   raise ValidationError('User not found')
   
   # Modified
   raise ValidationError(msg.get_error_message('USER_NOT_FOUND'))
   ```

3. **Handle Parameterized Messages**
   ```python
   # Original
   raise ValidationError(f'Lab has {count} research groups')
   
   # Modified
   raise ValidationError(msg.get_error_message('LAB_HAS_GROUPS', count=count))
   ```

## Extension Guide

### Adding New Messages

1. Add new key-value pairs to the appropriate dictionary in `messages.py`
2. Use descriptive key names (all uppercase, underscore separated)
3. For parameters, use `{param_name}` format

```python
# Add to Messages.SUCCESS or Messages.ERRORS
'NEW_OPERATION_SUCCESS': 'New operation executed successfully',
'CUSTOM_ERROR_MESSAGE': 'Custom error: {detail}',
```

### Internationalization Preparation

For future multi-language support, the `Messages` class can be extended:

```python
class Messages:
    def __init__(self, language='zh'):
        self.language = language
        self.messages = self._load_messages(language)
    
    def _load_messages(self, language):
        # Load different message files based on language
        pass
```

## Best Practices

1. **Unified Usage**: All new code should use unified message management
2. **Clear Semantics**: Message key names should clearly express meaning
3. **Consistent Parameters**: Use same naming for same type of parameters
4. **Categorical Management**: Organize messages by functional modules
5. **Documentation Updates**: Update this documentation when adding new messages

## Important Notes

- Don't directly modify message content; use parameterization for dynamic content
- Maintain consistency and readability of message key names
- Ensure all references are correctly updated during refactoring
- Test refactored functionality to ensure messages display correctly