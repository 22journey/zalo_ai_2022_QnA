import json
import time
import os
import codecs
from core import tokenize
from core import utils
from tqdm import tqdm
import pandas as pd


def process_line_to_token(text):
    # remove unused link
    idx = text.find("BULLET ::::")
    # print(idx)
    if idx > 0:
        text = text[:idx]
    return tokenize.token_and_score(text)


def partial_dictionary(filename, out):
    d = {}
    scored = {}
    with open(filename, 'r') as f:
        i = 0
        t = time.time()
        for l in f:
            text = json.loads(l)
            text = text["text"]
            token_dict = process_line_to_token(text)
            for k, score in token_dict.items():
                d[k] = d.get(k, 0) + 1
                scored[k] = max(scored.get(k, 0), score)
            i += 1
            if i % 100 == 0:
                print("%s: %s lines, run time %s\n" % (filename, i+1, time.time() - t))
        print("%s: %s lines, run time %s\n. Finished" % (filename, i+1, time.time() - t))
    ls = sorted(d.items(), key=lambda it: it[1], reverse=True)
    with codecs.open(out, "w", "utf-8") as f:
        for l in ls:
            f.write(json.dumps({
                "token": l[0],
                "score": scored[l[0]],
                "count": l[1],
            }, ensure_ascii=False))
            f.write("\n")


def partial_token_by_line(filename, out):
    lines = []
    with open(filename, 'r') as f:
        i = 0
        t = time.time()
        for l in f:
            raw = json.loads(l)
            text = raw["text"]
            token_dict = process_line_to_token(text)
            lines.append({
                "id": raw["id"],
                "tokens": token_dict,
            })
            i += 1
            if i % 100 == 0:
                print("%s: %s lines, run time %s\n" % (filename, i+1, time.time() - t))
        print("%s: %s lines, run time %s\n. Finished" % (filename, i+1, time.time() - t))

    with codecs.open(out, "w", "utf-8") as f:
        for l in lines:
            f.write(json.dumps(l, ensure_ascii=False))
            f.write("\n")


def merge_dictionary_from_partials_to_csv(folder, target_file):
    filenames, filepaths = utils.get_all_file_in_folder(folder)
    merged = {}
    for fp in tqdm(filepaths):
        print(fp)
        with open(fp, 'r') as f:
            for l in f:
                d = json.loads(l)
                if not tokenize.valid_token(d["token"]):
                    continue
                old = merged.setdefault(d["token"], {})
                old["token"] = d["token"]
                old["score"] = max(old.get("score", 0), d["score"])
                old["count"] = old.get("count", 0) + d["count"]
    ls = sorted(merged.values(), key=lambda it: it["count"], reverse=True)
    token, score, count = [], [], []
    for l in ls:
        token.append(l["token"])
        score.append(l["score"])
        count.append(l["count"])
    
    df = pd.DataFrame.from_dict({
        "token": token,
        "score": score,
        "count": count,
    })

    df.to_csv(target_file)
