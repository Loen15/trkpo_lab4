import json
import tiktoken

def message_to_text(message):
  if message['text'] != None:
    return message['text'] 
  if message['caption'] != None:
    return message['caption'] + 'также отправил вам фото'
  match message['media']:
    case 'MessageMediaType.STICKER':
      return message.sticker.emoji
    case 'MessageMediaType.PHOTO':
      return 'Отправил Вам фото документа'
    case 'MessageMediaType.DOCUMENT':
      return 'Отправил Вам документ'
    case 'MessageMediaType.AUDIO':
      return 'Отправил Вам аудиофайл' 
    case 'MessageMediaType.VIDEO':
      return 'Отправил Вам видео'
    case 'MessageMediaType.ANIMATION':
      return 'Отправил Вам гифку'
    case 'MessageMediaType.CONTACT':
      return 'Отправил Вам контакт'
    case 'MessageMediaType.LOCATION':
      return 'Отправил Вам локацию'
    case 'MessageMediaType.VENUE':
      return 'Отправил Вам место проведения'
    case 'MessageMediaType.POLL':
      return 'Отправил Вам опрос'
    case 'MessageMediaType.WEB_PAGE':
      return 'Отправил Вам ссылку'
    case 'MessageMediaType.GAME':
      return 'Отправил Вам игру'
    case 'MessageMediaType.DICE':
      return 'Кинул 6-гранный игральный кубик'
    case _:
      return ' '

name = 'чат с кем-то'
# функция генерирующая чат для GPT
with open(f'telegram raw/{name}.json', 'r', encoding='utf-8') as json_file:
  data = json.load(json_file)  
  msgs = [{"role":"system","content":"Ты Ваня, общайся в дружеской манере"}]
  is_self = 'user546555037' # вставить свой id из файла
  for msg in data['messages']:
    msgs.append({"role":"assistant" if msg['from_id'] == is_self else "user","content": message_to_text(msg)})  
  string = '{"messages":[\n'
  for item in msgs:
    string += json.dumps(item, ensure_ascii=False) + ",\n" 
  string = string[:-2]+'\n]}'   
  encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0125")
  count = len(msgs)
  count_tokens = len(encoding.encode(string))
  print('количество сообщений: ' + str(count))
  print('количество токенов: ' + str(count_tokens))
  with open(f"ready/telegram/{name}_msg-{count}_tkns-{count_tokens}_with-n.json", 'w', encoding='utf-8') as f:
    f.write(string)

