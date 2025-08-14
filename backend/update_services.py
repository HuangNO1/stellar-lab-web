# Script to add image upload management to description field services
import os
import re

def add_image_upload_import(file_path):
    """Add ImageUploadService import to a service file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if import already exists
    if 'from .image_upload_service import ImageUploadService' in content:
        return False
    
    # Add import after base_service import
    pattern = r'(from \.base_service import BaseService.*?\n)'
    replacement = r'\1from .image_upload_service import ImageUploadService\n'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

def add_image_management_to_create(file_path, entity_type, desc_fields):
    """Add image management logic to create methods"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if image management already exists
    if 'image_upload_service.mark_images_as_used' in content:
        return False
    
    # Find the location after self.db.session.flush() in create methods
    pattern = r'(self\.db\.session\.flush\(\)\s*\n)'
    
    image_logic = f'''            
            # 處理描述字段中的圖片管理
            image_upload_service = ImageUploadService()
            for field in {desc_fields}:
                if field in data and data[field]:
                    image_upload_service.mark_images_as_used(
                        content=data[field],
                        entity_type='{entity_type}',
                        entity_id=entity.{entity_type}_id,
                        field_name=field
                    )
'''
    
    replacement = r'\1' + image_logic + '\n'
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return True
    return False

# Services to update with their entity types and description fields
services_to_update = [
    ('/home/rem/Documents/Study/Code/lab_web/backend/app/services/lab_service.py', 'lab', "['lab_desc_zh', 'lab_desc_en']"),
    ('/home/rem/Documents/Study/Code/lab_web/backend/app/services/member_service.py', 'member', "['mem_desc_zh', 'mem_desc_en']"),
    ('/home/rem/Documents/Study/Code/lab_web/backend/app/services/project_service.py', 'project', "['project_desc_zh', 'project_desc_en']"),
    ('/home/rem/Documents/Study/Code/lab_web/backend/app/services/research_group_service.py', 'research_group', "['research_group_desc_zh', 'research_group_desc_en']")
]

for file_path, entity_type, desc_fields in services_to_update:
    if os.path.exists(file_path):
        print(f"Updating {file_path}...")
        
        # Add import
        import_added = add_image_upload_import(file_path)
        if import_added:
            print(f"  - Added ImageUploadService import")
        
        # Add image management to create methods
        # Note: This is a simplified approach - in practice we'd need more sophisticated parsing
        print(f"  - Manual update needed for create/update methods")
    else:
        print(f"File not found: {file_path}")

print("Script complete. Manual updates still needed for create/update method logic.")