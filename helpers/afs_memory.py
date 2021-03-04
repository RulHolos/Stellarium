import os, io, json, zipfile, datetime, pickle, functools
from cryptography.fernet import Fernet
from discordDBPlus import DiscordDB
from discordDBPlus.models import Data
from benedict import benedict

# Construction d'un objet json par rapport à load_afs_memory
class const_json:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

# Construction d'un objet Data par rapport à load_afs_memory
class const_DiscordDBPlus_Data:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        self.constr_json = const_json(self.filename, self.content)
        self.data = Data(content=self.constr_json.content, created_at=datetime.datetime.today())

class pickle_afs_object:
    def __init__(self, filename, input_data):
        self.filename = filename
        self.input_data = input_data
        self.constr = self.construct()

    def construct(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.input_data, f)

class afs_memory:
    def __init__(self, file):
        self.file = file
        self.key = Fernet("Generate your own fernet key plz.")

        with open(self.file, 'rb') as enfile:
            self.enf = enfile.read()

        self.defile = self.key.decrypt(self.enf)
        self.filent = io.BytesIO(self.defile)
        self.listfiles = {}
        self.construct_memory_data()
        self.contents = self.read_files_content()

        self.supports = ' ; '.join(["json (fully)", "plain text", "DiscordDBPlus.Data"])
        self.j_load = json.loads(self.construct_json().content) # Une façon plus digest d'accéder à in_data pour les modify memory data

    def construct_memory_data(self):
        with zipfile.ZipFile(io.BytesIO(self.defile)) as thezip:
            for zipinfo in thezip.infolist():
                with thezip.open(zipinfo) as thefile:
                    self.listfiles[zipinfo.filename] = thefile

    def read_files_content(self):
        contentlist = []
        for keya, value in self.listfiles.items():
            with zipfile.ZipFile(self.filent) as f:
                with f.open(keya) as f2:
                    if value != '':
                        contentlist.append(f2.read())
                    else:
                        pass
        return contentlist

    def construct_json(self):
        constr = const_json(self.file, self.contents[0].decode("utf-8"))
        return constr

    def construct_DiscordDBPlus_Data(self):
        constr = const_DiscordDBPlus_Data(self.file, self.contents[0].decode("utf-8"))
        return constr

    def construct_pickle(self, filename):
        """
        Doesn't supports Data object at the time being.
        """
        constr = pickle_afs_object(filename, self.contents[0].decode("utf-8"))

    def load_afs_pickle(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


    def modify_values_helper(self, out_file):
        split = os.path.splitext(self.file)[0]

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as f:
            f.writestr(split, out_file.read())
        with open(f"{split}.zip", 'wb') as f:
            f.write(zip_buffer.getvalue())
        with open(f"{split}.zip", 'rb') as f:
            value = f.read()

        enfile = self.key.encrypt(value)

        with open (f'{split}.afs', 'wb') as encrypted_file:
            encrypted_file.write(enfile)
        os.remove(f'{split}.zip')

    def write_json_to_afs(self, in_data, new_data):
        """
        Used for json format only

        Parameters
        -----------
        in_data
            content state

        new_data
            dict de key et value
        """
        for key, values in new_data.items(): # Ajoute et modifie les valeurs
            in_data[key] = values

        res_data = json.dumps(in_data).encode("utf-8")
        out_file = io.BytesIO(res_data)
        self.modify_values_helper(out_file)

    def delete_json_from_afs(self, in_data, del_data):
        """
        Used for json format only
        Deletes keys (and its values) from a json

        Parameters
        -----------
        in_data
            content state

        del_data
            list de keys à supprimer
        """

        in_data = benedict(in_data)
        in_data.pop(del_data)

        res_data = json.dumps(in_data).encode("utf-8")
        out_file = io.BytesIO(res_data)
        self.modify_values_helper(out_file)


#a = afs_memory("test.json.afs")
#print(a.construct_json().content)
#print(json.loads(a.contents[0].decode("utf-8"))['692853537813823580']) #Permet de convertir de la data en json
#a.construct_pickle("chips")
#print(a.load_afs_pickle("chips"))
#a.write_json_to_afs(a.j_load, {"test": "un valeur au hasard"})
#a.delete_json_from_afs(a.j_load, ["Valeur 1", "Valeur 2"])
#print(a.construct_json().content)
