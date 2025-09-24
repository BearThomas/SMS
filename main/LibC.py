# LibC.py

import os, base64

class Table():
    def __init__(self, data=None, name=None, keys=None):
        self.data = data if data is not None else [[]]
        self.name = name
        self.keys = keys if keys is not None else []
        self.keys_map = {}

        count = 0
        for key in self.keys:
            self.keys_map[key] = count
            count += 1
    
    def find(self, keys_name=None, data=None):
        if keys_name is None:
            keys_name = []
        if data is None:
            data = []
            
        row_index = 0
        for row in self.data:
            is_this = True
            for key_index in range(len(keys_name)):
                if row[self.keys_map[keys_name[key_index]]] != data[key_index]:
                    is_this = False
                    break
            if is_this:
                return row_index
            row_index += 1
        
        return None
    
    def delete(self, row_index):
        try:
            del self.data[row_index]
        except IndexError:
            print(f"Error: Row index {row_index} out of range")

    def add(self, data=None, row=-1):
        if data is None:
            data = []
            
        if len(data) != len(self.keys):
            print(f"Error: Data length {len(data)} doesn't match keys length {len(self.keys)}")
            return
            
        try:
            self.data.insert(row, data)
        except Exception as e:
            print(f"Error inserting data: {e}")

    def change(self, row, key_name, new_Data):
        self.data[row][self.keys_map[key_name]] = new_Data
    
    def at(self, row, key_name):
        return self.data[row][self.keys_map[key_name]]

    def sort(self, key, direction=True, data=None):
        if data is None:
            data = self.data
            
        if key not in self.keys_map:
            raise KeyError(f"Key '{key}' not found in table")
        
        if len(data) <= 1:
            return data.copy()
        
        mid = len(data) // 2
        L = data[:mid]
        R = data[mid:]
        
        L_sorted = self.sort(key, direction, L)
        R_sorted = self.sort(key, direction, R)
        
        res = []
        i = j = 0
        
        if direction:
            while i < len(L_sorted) and j < len(R_sorted):
                if L_sorted[i][self.keys_map[key]] <= R_sorted[j][self.keys_map[key]]:
                    res.append(L_sorted[i])
                    i += 1
                else:
                    res.append(R_sorted[j])
                    j += 1
        else:
            while i < len(L_sorted) and j < len(R_sorted):
                if L_sorted[i][self.keys_map[key]] >= R_sorted[j][self.keys_map[key]]:
                    res.append(L_sorted[i])
                    i += 1
                else:
                    res.append(R_sorted[j])
                    j += 1
        
        while i < len(L_sorted):
            res.append(L_sorted[i])
            i += 1
            
        while j < len(R_sorted):
            res.append(R_sorted[j])
            j += 1
        
        return res 

    def clear(self):
        self.data = [[]]
    

class Lib():
    def __init__(self, path='./NewLib.xLib'):
        self.path = path
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.write('&EMPTY&')

        self.tables_read = []
        self.tables = []

        with open(path, 'r') as file:
            file_read = file.read()
            # print(base64.b85decode(file_read).decode())
            if (file_read == '&EMPTY&'):
                return 
            # print(file_read)
            file_read = base64.b85decode(file_read).decode()
            # print(file_read)
            self.tables_text = file_read.split('&table&')
            # print(self.tables_text)
        
        for table_text in self.tables_text:
            if table_text == '&EMPTY&':
                continue
                
            table_info = ['', [], []]
            parts = table_text.split('&Name&')
            if len(parts) > 1:
                table_info[0] = parts[0]
                key_part = parts[1].split('$KeyEnd$')[0]
                table_info[1] = key_part.split('&Key&')[:-1]
                
                row_parts = table_text.split('$')[1:]
                for row_part in row_parts:
                    if '#' in row_part:
                        row_data = row_part.split('#')[1:]
                        row_data = list(map(self.to_int, row_data))
                        table_info[2].append(row_data)
            
            self.tables_read.append(table_info)

        for table_info in self.tables_read:
            self.tables.append(Table(table_info[2], table_info[0], table_info[1]))

    def crTabel(self, name, Keys):
        self.tables.append(Table(name=name, keys=Keys))
    
    def close(self):
        self.save()

    def save(self):
        if not self.tables:
            with open(self.path, 'w') as file:
                file.write('&EMPTY&')
            return
        
        tables_content = []
        for table in self.tables:
            table_str = table.name if table.name else ""
            table_str += "&Name&"
            
            if table.keys:
                table_str += "&Key&".join(table.keys) + "&Key&"
            table_str += "$KeyEnd$"
            
            for row in table.data:
                table_str += "$"
                if row:
                    table_str += "#" + "#".join(str(field) for field in row)
            
            tables_content.append(table_str)
        
        full_content = "&table&".join(tables_content)
        encoded_content = base64.b85encode(full_content.encode()).decode()
        
        with open(self.path, 'w') as file:
            file.write(encoded_content)
     
    def table(self, name=None):
        for table in self.tables:
            if table.name == name:
                return table
        return None
    
    def to_int(self, text):
        try:
            return int(text)
        except:
            return text