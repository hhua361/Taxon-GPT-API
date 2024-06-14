# 可能有用需要尝试的东西：
  #  messages.append({"role": "assistant", "content": response.choices[0].message.content)
  #  prompt = “”
  #  messages.append({"role": "assistant", "content":prompt})
  # 通过这种方法来生成一步一步的结果，例如第一步计算出first character 以及对应的subgroup，然后再次调回只对某个subgroup来进行计算
  # 我感觉我对于API的使用还有很多东西需要学习
  # 如何设置循环是一个非常关键的过程，我希望实现的是分别提供数据集和prompt内容，通过对应的taxa，name，这是否需要我考虑到使用需要鉴别taxa的名称，但是关键是我需要如何确定所有的subgroup是完全分开的，存在几个可能的关键问题
  # 首先我无法确认；通过initial character究竟能分出几个subgroup。同时对每个subgroup中进行继续的再分，也需要确认如何分类，需要设置标识符来进行分别

import json
from openai import OpenAI
import os
### part 1 选择合适的initial character，之后所有的结果可以根据这个初始结果进行分析，目前我在prompt部分设置了一个部分的内容，将通过选择初始character的结果存储在# initail character classify result #中，后续可以通过添加代码在这个附近，提取出这个block的信息

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# using the prompt and dataset to calculate the initial character, save the initial character information and classifiction situation
with open("D:/桌面/TEST-KG/nexus fix/matrix_knowledge_graph_22.json", "r", encoding="utf-8") as file:
    matrix_data = json.load(file)
matrix_data_str = json.dumps(matrix_data, ensure_ascii=False)
messages = [{"role":"system",
             "content":
                 "You are a helpful taxonomist assistant."+ \
                 "You are skilled at calculating the correct information gain to choose the character that best divides species into even groups based on their states." +\
                 "Based on the selected character, classify the species into different groups according to their states." + \
                 "For each group with more than two species, continue selecting characters to further classify this group until each group only has one species." + \
                 "After multiple classifications, determine the final classification levels and record each classifying character and its state. " + \
                 "Finally, generate a taxonomic key."},
            {"role":"user",
            "content": """
                Generate the taxonomic key based on the provided morphological matrix. The matrix includes all species and their different states for each character.\n
                The process involves selecting a character to classify the species into groups. Repeat this classification within each subgroup until each group contains only one species.\n
                Information gain measures how much the uncertainty in the dataset is reduced after using a character for classification. It helps in selecting characters that minimize the entropy of the subset after classification, leading to better classification results.\n
                Please select the initial classification character for all species based on the morphological matrix and information gain methods.\n
                In the morphological matrix, 'Missing' and 'Not applicable' are invalid states. If a character has invalid states for the group being classified, it should be ignored.\n
                States are represented by numbers, and like the '1,2' means multiple states should be treated as a single state type. The initial character should have no more than three state types.\n
                you need to calculate the information gain for each character, and choose the highest inforamtion gain result, The higher the Information Gain result, the greater the contribution of the feature to the classification.\n
                Now I will show you the morphological matrix. Please provide only the initial classification character and the categorization of species based on its state, and you should signlely show this called as # initail character classify result # 
            """},
            {"role": "assistant",
            "content": """
                Understood. I will generate the taxonomic key based on the provided morphological matrix. Here is a summary of the steps I will follow:\n
                1. The matrix includes all species and their different states for each character.\n
                2. I will select a character to classify the species into groups and repeat this classification within each subgroup until each group contains only one species.\n
                3. I will use information gain to measure how much the uncertainty in the dataset is reduced after using a feature for classification. This helps in selecting features that minimize the entropy of the subset after classification, leading to better classification results.\n
                4. I will select the initial classification character for all species based on the morphological matrix and information gain methods.\n
                5. In the morphological matrix, 'Missing' and 'Not applicable' are considered invalid states. If a character has invalid states for the group being classified, it will be ignored.\n
                6. States are represented by numbers. For example, '1 and 2' means multiple states should be treated as a single state type. The initial character should have no more than three state types.\n
                7. I will use information gain to calculate all character and choose the highest inforamtion gain result, The higher the Information Gain result, the greater the contribution of the feature to the classification. \n
                8. The final result will provide only the initial classification character and the categorization of species based on its state, and i will named result called # initail character classify result # \n
                Please provide the morphological matrix data so that I can proceed with the initial classification.
            """
            },
            {"role":"user",
             "content":
                 f"Here is morphological matrix:{matrix_data_str}"}
            ]
initial_character_info =  client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        max_tokens=1500,
        temperature=0,
        n = 1)
# 但是实际上在中间这个部分中还需要加上的调取出这个额外的信息，
# based on the for the subgroup species to do continue classify
initial_response = initial_character_info.choices[0].message.content
messages = [{"role": "assistant", "content": initial_response}]
prompt = ""
messages.append({"role": "assistant", "content":prompt})
response =  client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stop=None,
        temperature=0,
        stream =True,
        n = 1
)