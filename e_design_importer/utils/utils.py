import os
import re


class FolderScanner:
    def __init__(self, root_path):
        self.root_path = root_path
        self.cat_pattern = re.compile(r'^(.*?)\s*\(CAT-(.+?)\)$')
        self.sub_pattern = re.compile(r'^(.*?)\s*\(SUB-(.+?)\)$')
        self.prod_pattern = re.compile(r'^(.*?)\s*\(PROD-(.+?)\)$')
        self.des_pattern = re.compile(r'^(.*?)\s*\((?:DES|DIS)-(.+?)\)$')
    
    def scan(self):
        result = {
            'categories': [],
            'subcategories': [],
            'designs': [],
            'products': []
        }
        
        for item in os.listdir(self.root_path):
            item_path = os.path.join(self.root_path, item)
            
            if not os.path.isdir(item_path):
                continue
                
            cat_match = self.cat_pattern.match(item)
            if cat_match:
                self._process_category(item_path, cat_match, result)
        
        return result
    
    def _process_category(self, cat_path, cat_match, result):
        cat_name = cat_match.group(1).strip()
        cat_code = cat_match.group(2).strip()
        
        result['categories'].append({
            'name': cat_name,
            'code': cat_code,
            'path': cat_path
        })
        
        for sub_item in os.listdir(cat_path):
            sub_path = os.path.join(cat_path, sub_item)
            if not os.path.isdir(sub_path):
                continue
            
            sub_match = self.sub_pattern.match(sub_item)
            if sub_match:
                self._process_subcategory(sub_path, sub_match, cat_code, result)
            
            prod_match = self.prod_pattern.match(sub_item)
            if prod_match:
                self._process_product(sub_path, prod_match, result)
        
        self._scan_designs(cat_path, cat_code, result['designs'])
    
    def _process_subcategory(self, sub_path, sub_match, parent_code, result):
        sub_name = sub_match.group(1).strip()
        sub_code = sub_match.group(2).strip()
        
        result['subcategories'].append({
            'name': sub_name,
            'code': sub_code,
            'parent_code': parent_code,
            'path': sub_path
        })
        
        self._scan_designs(sub_path, sub_code, result['designs'])
        self._scan_products_in_folder(sub_path, result)
    
    def _process_product(self, prod_path, prod_match, result):
        prod_name = prod_match.group(1).strip()
        prod_code = prod_match.group(2).strip()
        
        designs = []
        self._scan_designs(prod_path, None, designs)
        
        result['products'].append({
            'name': prod_name,
            'code': prod_code,
            'path': prod_path,
            'designs': designs
        })
    
    def _scan_products_in_folder(self, folder_path, result):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if not os.path.isdir(item_path):
                continue
            
            match = self.prod_pattern.match(item)
            if match:
                self._process_product(item_path, match, result)
    
    def _scan_designs(self, folder_path, category_code, designs_list):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if not os.path.isdir(item_path):
                continue
            
            match = self.des_pattern.match(item)
            if match:
                designs_list.append({
                    'name': match.group(1).strip(),
                    'code': match.group(2).strip(),
                    'category_code': category_code,
                    'path': item_path
                })