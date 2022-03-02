from flask import Flask
import openai
import json
import os

openai.api_key = os.environ.get('OPENAI')

def callAPI(input_prompt, engine_type="text-davinciplus-001", temp=0.2):
    try:
        output = openai.Completion.create(
          engine=engine_type,
          prompt=input_prompt,
          max_tokens=250,
          temperature=temp,
          n=1,
          stop="\n\n"
        )
        output = json.dumps(output)
        output = json.loads(output)['choices'][0]
        for ind in output:
            if (ind == 'text'):
                output = output[ind]
                return output
            else:
                print('Error: failed to find text in output')
                raise RuntimeError
    except:
        print('Error: failed to make successful OpenAI API call')
        print(output)
        raise RuntimeError

def makeValues(text_array):
    print(text_array)
    try:
        output = {}
        for text in text_array:
            if text == '':
                pass
            else:
                split_text = text.split(": ", 1)
                if split_text[1] == "none" or split_text[1] == "None":
                    output[str(split_text[0])] = ""
                else:
                    output[str(split_text[0])] = split_text[1].strip()
        return output

    except:
        print("error converting array values to dict")
        print(output)
        print(text)
        raise RuntimeError


app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return "Welcome to Midas"

@app.route('/company/<input>', methods=["GET"])
def company(input=None):
    if not input:
        return "Error: Please supply a company's name"
    else:
        company_text="Fill in the company facts table truthfully.  If unsure list none.\n---\nFord\nstock_symbol: F\nstock_market: NYSE\nceo: Jim Farley\nheadquarters: Dearborn, MI\nindustry: automotive, manufacturing, electric vehicle\nfounded_date: 1903\nfounders: Henry Ford\nlegal_name: Ford Motor Company\ncompany_website: https://ford.com\nsummary: Ford Motor Company is an American multinational automobile manufacturer headquartered in Dearborn, Michigan, United States.\ncompetitors: Chevrolet, Toyota, Honda\nwikipedia_url: https://en.wikipedia.org/wiki/Ford_Motor_Company\ncrunchbase_url: https://www.crunchbase.com/organization/ford\ninstagram_url: https://www.instagram.com/ford\ntwitter_url: https://twitter.com/Ford\nyoutube_url: https://www.youtube.com/user/ford\n---\n"
        loaded_prompt=company_text+input
        engine_used="text-davinciplus-001"
        result=callAPI(loaded_prompt, engine_used, 0.2)
        result = result.split('\n')
        formatted_result=makeValues(result)
        try:
            final={}
            final['triples']={}
            final['metadata']={}
            final['subject']=input
            final['type']='company'
            final['triples']['stock_symbol'] = formatted_result['stock_symbol']
            final['triples']['stock_market'] = formatted_result['stock_market']
            final['triples']['ceo'] = formatted_result['ceo']
            final['triples']['industry'] = formatted_result['industry'].split(',')
            final['triples']['headquarters'] = formatted_result['headquarters']
            final['triples']['founded_date'] = formatted_result['founded_date']
            final['triples']['founders'] = formatted_result['founders'].split(',')
            final['triples']['legal_name'] = formatted_result['legal_name']
            final['triples']['company_website'] = formatted_result['company_website']
            final['triples']['wikipedia_url'] = formatted_result['wikipedia_url']
            final['triples']['summary'] = formatted_result['summary']
            final['metadata']['producer']='MIDAS v0.01'
            final['metadata']['nlp_model']=engine_used
            print(final)
            json_result = json.dumps(final)
        except:
            print('Error: could not form JSON from key:values')
            print(formatted_result)
            return '{"Error": "could not form JSON from key:values"}'
        return json_result


@app.route('/person/<input>', methods=["GET"])
def person(input=None):
    if not input:
        return "Error: Please supply a company's name"
    else:
        company_text="Fill in the persons fact table truthfully.  If unsure list none.\n---\nFord\nstock_symbol: F\nstock_market: NYSE\ncommon_name: Jim Farley\nborn: 1956\nlegal_name: Jim Farley\nsummary: Jim Farley is the CEO of Ford Motor Company.\nwikipedia_url: https://en.wikipedia.org/wiki/Jim_Farley\ninstagram_url: https://www.instagram.com/ford\ntwitter_url: https://twitter.com/Ford\nyoutube_url: https://www.youtube.com/user/ford\n---\n"
        loaded_prompt=company_text+input
        engine_used="text-davinciplus-001"
        result=callAPI(loaded_prompt, engine_used, 0)
        result = result.split('\n')
        formatted_result=makeValues(result)
        final={}
        final['triples']={}
        final['metadata']={}
        final['subject']=input
        final['type']='person'
        final['triples']['common_name'] = formatted_result['common_name']
        final['triples']['born'] = formatted_result['born']
        final['triples']['legal_name'] = formatted_result['legal_name']
        final['triples']['instagram_url'] = formatted_result['instagram_url']
        final['triples']['twitter_url'] = formatted_result['twitter_url']
        final['triples']['wikipedia_url'] = formatted_result['wikipedia_url']
        final['triples']['summary'] = formatted_result['summary']
        final['metadata']['producer']='MIDAS v0.01'
        final['metadata']['nlp_model']=engine_used
        print(final)
        json_result = json.dumps(final)
        return json_result
