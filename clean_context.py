from core.context import clean
# from concurrent.futures import ProcessPoolExecutor
import os
import sys
from core import define


partials_folder = define.CONTEXT_PARTIALS_FOLDER
output_folder = define.CONTEXT_FOLDER
max_worker = 2


def process_file_dict(file_name):
    file_path = os.path.join(partials_folder, file_name)
    tmp_folder = os.path.join(output_folder, ".tmp")
    print("Process file " + file_name)
    file_out = os.path.join(tmp_folder, file_name + ".processed")
    clean.partial_dictionary(file_path, file_out)
    print("Done process file %s, output to %s" % (file_path, file_out))


def process_file_token(file_name):
    tmp_folder = os.path.join(output_folder, ".token")
    try:
        os.makedirs(tmp_folder)
    except:
        pass
    file_path = os.path.join(partials_folder, file_name)
    print("Process file " + file_name)
    file_out = os.path.join(tmp_folder, file_name + ".processed")
    clean.partial_token_by_line(file_path, file_out)
    print("Done process file %s, output to %s" % (file_path, file_out))

# def process_all_token(in_folder, out_folder):
#     tmp_folder = os.path.join(out_folder, ".tmp")
#     try:
#         os.makedirs(tmp_folder)
#     except:
#         pass

#     partials = []
#     for _, _, files in os.walk(in_folder):
#         partials = [(os.path.join(in_folder, f), f) for f in files]
#         break

#     partials = partials[:2]

#     with ProcessPoolExecutor(max_worker) as exe:
#         exe.map(process_file, partials)
#     # process_file(partials[0][0], partials[0][1])


# process_file_dict(sys.argv[1])
# process_file_token(sys.argv[1])

clean.merge_dictionary_from_partials_to_csv(
    os.path.join(output_folder, ".tmp"),
    os.path.join(output_folder, "merged_tokens.csv")
)



