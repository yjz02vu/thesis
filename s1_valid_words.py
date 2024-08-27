import json
import os 

dir_conver = "predefined_data"
os.makedirs(dir_conver, exist_ok=True)
#valid words list

# Define your custom valid words
custom_valid_words = {
    'smiley', 'healthcare', 'grandkids', 'hang', 'nonverbally', 'bible', 'email', 'handwritten', 'brings', 'tv', 'smartphone', 'app', 'okay', 'fond', 'audiobooks', "others", 'surreal', 'backyard', 'anymore', 'wheelchair', 've', 'coordination','pt', 'skincare', 'hon', 'yogurt', 'moisturize', 'sunscreen', 'restroom', 'chamomile', 'ct'}

# Define the file path to store the custom words
custom_words_file = "custom_valid_words.json"
file_path = os.path.join(dir_conver, custom_words_file)


# Save the custom valid words to a JSON file
def save_pred_data(words, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(words, file, indent=4)
    print(f"Predefined data saved to '{file_path}' successfully!")


save_pred_data(list(custom_valid_words), file_path)

# ICF categories and definition

custom_icf_file = "icf_cate_comb.json"
file_path_icf = os.path.join(dir_conver, custom_icf_file)


ICF_cate_comb = {
    "mobility": {
        "Changing basic body position": {
            "definition": "Getting into and out of a body position and moving from one location to another",
            "examples": "Getting up out of a chair to lie down on a bed; getting into and out of positions of sitting, standing, kneeling such as during prayers; squatting such as in toilets that are at floor level; bending such as in bowing or reaching down for an object.",
            
            "sub_activity": "Lying down; Squatting; Kneeling; Sitting; Standing; Bending; Shifting the body's centre of gravity; Rolling over."
        },
        "Maintaining body position": {
            "definition": "Staying in the same body position as required",
            "examples": "Remaining seated or remaining standing for carrying out a task, in play, work or school; remaining in a lying position; remaining in a squatting position; remaining in a kneeling position such as during prayers in church; maintaining a sitting position such as when sitting at a desk or table; remaining in a standing position such as when standing in a queue; remaining the head position"
        },
        "Transferring oneself": {
            "definition": "Moving from one surface to another",
            "examples": "Sliding along a bench or moving from a bed to a chair, without changing body position."
        },
        "Lifting and carrying objects": {
            "definition": "Moving from a sitting position on one seat to another seat on the same or a different level.",
            "examples": "Moving from a chair to a bed; lifting such as lifting a glass from the table; carrying in the hands such as when carrying a drinking glass or a suitcase; carrying in the arms such as when carrying a pet or a child or other large object; carrying on shoulders, hip and back, such as when carrying a large parcel or school-bag; carrying on the head such as when carrying a container of water on the head; putting down objects such as when lowering a container of water to the ground."
        },
        "Moving objects with lower extremities": {
            "definition": "Performing coordinated actions aimed at moving an object by using the legs and feet",
            "examples": "Kicking a ball; pushing pedals on a bicycle; pushing a chair away with a foot.",
            "sub_activity": "Using the legs and feet to exert a force on an object to move it away; Using the legs and feet to propel something away"
        },
        "Fine hand use": {
            "definition": "Performing the coordinated actions of handling objects, picking up, manipulating and releasing them using one's hand, fingers and thumb",
            "examples": "Lifting coins off a table; turning a dial or knob; picking up a pencil; grasping a tool or a door knob; handling coins or other small objects, such as scissors, shoe laces, pencils, chop sticks, knives and forks; dropping an item of clothing or a piece of food for a pet.",
            "sub_activity": "Lifting or taking up a small object with hands and fingers; Using one or both hands to seize and hold something; Using fingers and hands to exert control over, direct or guide something; Using fingers and hands to let go or set free something so that it falls or changes position"
        },
        "Hand and arm use": {
            "definition": "Performing the coordinated actions required to move objects or to manipulate them by using hands and arms, such as when turning door handles or throwing or catching an object.",
            "examples": "Pulling on a string or pulling a door closed, pushing a toy or an animal away, reaching across a table or desk for a book, as is required to open a jar or use tools such as a toothbrush or screwdriver, tossing a ball, catching a ball.",
            "sub_activity": "Using fingers, hands and arms to bring an object towards or from oneself; to extend outwards and touch and grasp something; to rotate, turn or bend an object; to lift something and propel it with some force through the air; to grasp a moving object in order to bring it to a stop and hold it."
        },
        "Fine foot use": {
            "definition": "Performing the coordinated actions to move or manipulate objects using one's foot and toes."
        },
        "Walking": {
            "definition": "Moving along a surface on foot, step by step, so that one foot is always on the ground.",
            "examples": "Strolling, sauntering, walking forwards, backwards, or sideways.",
            "sub_activity": (
                "Walking short distances: Walking for less than a kilometre, such as walking around rooms or hallways, within a building or for short distances outside;\n"
                "Walking long distances: Walking for more than a kilometre, such as across a village or town, between villages or across open areas;\n"
                "Walking on different surfaces: Walking on sloping, uneven, or moving surfaces, such as on grass, gravel or ice and snow, or walking aboard a ship, train or other vehicle;\n"
                "Walking around obstacles: Walking in ways required to avoid moving and immobile objects, people, animals, and vehicles, such as walking around a marketplace or shop, around or through traffic or other crowded areas."
            )
        },
        "Going up and down stairs": {
            "definition": "Moving upwards and downwards so that at least one foot is always on the ground such as ascending and descending stairs or curbs.",
            "examples": "Walking around a marketplace or shop, around or through traffic or other crowded areas."
        },
        "Moving around": {
            "definition": "Moving the whole body from one place to another by means other than walking",
            "examples": "Climbing over a rock or running down a street, skipping, scampering, jumping, somersaulting or running around obstacles",
            "sub_activity": "Moving the whole body on hands, or hands and arms, and knees; Moving the whole body upwards or downwards; Moving with quick steps; Moving up off the ground by bending and extending the legs; Propelling the whole body through water by means of limb and body movements"
        },
        "Moving around in different locations": {
            "definition": "Walking and moving around in various places and situations.",
            "examples": "Walking between rooms in a house, within a building, or down the street of a town, moving around other people's homes, other private buildings, community and public buildings and enclosed areas, walking for short or long distances around a town or village."
        },
        "Moving around using equipment": {
            "definition": "Moving the whole body from place to place, on any surface or space, by using specific devices designed to facilitate moving or create other ways of moving around.",
            "examples": "With skates, skis, or scuba equipment, or moving down the street in a self-propelled wheelchair or a walker"
        },
        "Using transportation": {
            "definition": "Using transportation to move around as a passenger.",
            "examples": "Being driven in a car, bus, rickshaw, jitney, pram or stroller, wheelchair, animal-powered vehicle, private or public taxi, train, tram, subway, boat or aircraft and using humans for transportation,  by car, taxi or privately owned aircraft or boat, being crried in the arms, in a sheet, in a backpack or a transportation device."
        },
        "Driving": {
            "definition": "Being in control of and moving a vehicle or the animal that draws it, travelling under one's own direction or having at one's disposal any form of transportation appropriate for age.",
            "examples": "A car, bicycle, boat or animal powered vehicles, a bicycle, tricycle, or rowboat, an automobile, motorcycle, motorboat or aircraft, an automobile, motorcycle, motorboat or aircraft."
        },
        "Riding animals for transportation": {
            "definition": "Travelling on the back of an animal.",
            "examples": "Such as a horse, ox, camel or elephant."
        }
    },


    
"communication": {
    "Communicating with receiving spoken messages": {
        "definition": "Comprehending literal and implied meanings of messages in spoken language.",
        "examples": "Understanding that a statement asserts a simple fact, a complex fact, an idiomatic expression or human voice without literal meaning.",
        "sub_activities": (
            "Comprehending the literal meaning conveyed by simple spoken messages;\n"
            "Comprehending the literal and implied meaning conveyed by complex spoken messages;\n"
            "Comprehending the human voice or sound without literal meaning."
        )
    },
    "Communicating with receiving nonverbal messages": {
        "definition": "Comprehending the literal and implied meanings of messages conveyed by gestures, symbols and drawings.",
        "examples": (
            "Realizing that a child is tired when she rubs her eyes or that a warning bell means there is a fire; comprehending traffic signs, warning symbols, musical or scientific notations, and icons; comprehending line drawings, graphic designs, paintings, three-dimensional representations, pictograms, graphs, charts and photographs, such as understanding that an upward line on a height chart indicates that a child is growing."
        ),
        "sub_activities": (
            "Comprehending the meaning conveyed by facial expressions, hand movements or signs, body postures, and other forms of body language;\n"
            "Comprehending the meaning represented by public signs and symbols;\n"
            "Comprehending the meaning represented by drawings."
        )
    },
    "Communicating with receiving formal sign language messages": {
        "definition": "Receiving and comprehending messages in formal sign language with literal and implied meaning."
    },
    "Communicating with receiving written messages": {
        "definition": "Comprehending the literal and implied meanings of messages that are conveyed through written language (including Braille).",
        "examples": "Following political events in the daily newspaper or understanding the intent of religious scripture."
    },
    "Speaking": {
        "definition": "Producing words, phrases and longer passages in spoken messages with literal and implied meaning.",
        "examples": "Expressing a fact or telling a story in oral language."
    },
    "Non-speech vocal expression": {
        "definition": "Vocalising when aware of another person in the proximal environment, such as making a sound when the mother is close; babbling; babbling in turn-taking activities. Vocalising in response to speech through imitating speech-sounds in a turn taking procedure."
    },
    "Singing": {
        "definition": "Producing tones in a sequence resulting in a melody to convey messages."
    },
    "Producing nonverbal messages": {
        "definition": "Using gestures, symbols and drawings to convey messages.",
        "examples": (
            "Shaking one's head to indicate disagreement; drawing a picture or diagram to convey a fact or complex idea; facial gestures (e.g. smiling, frowning, wincing); arm and hand movements, and postures (e.g. embracing to indicate affection or pointing to receive attention or an object); expressing by icons, Bliss board, scientific symbols; using musical notation to convey a melody; drawing a map to give someone directions to a location."
        )
    },
    "Producing messages in formal sign language": {
        "definition": "Conveying, with formal sign language, literal and implied meaning."
    },
    "Writing messages": {
        "definition": "Producing the literal and implied meanings of messages that are conveyed through written language, such as writing a letter to a friend."
    },
    "Conversation": {
        "definition": "Starting, sustaining and ending an interchange of thoughts and ideas, carried out by means of spoken, written, signed or other forms of language, with one or more people one knows or who are strangers, in formal or casual settings.",
        "sub_activities": (
            "Starting a conversation: Beginning an interchange, such as initiating turn-taking activity through eye-contact or other means, that leads to communication or dialogue, such as by introducing oneself, expressing customary greetings, or by introducing a topic or asking questions.\n"
            "Sustaining a conversation: Continuing an interchange by taking turns in vocalising, speaking or signing, by adding ideas, introducing a new topic or retrieving a topic that has been previously mentioned.\n"
            "Ending a conversation: Finishing a dialogue or interchange with customary termination statements or expressions and by bringing closure to the topic under discussion.\n"
            "Conversing with one person: Initiating, maintaining, shaping and terminating a dialogue or interchange with one person, such as in pre-verbal or verbal play, vocal or verbal exchange between mother and child, or in discussing the weather with a friend.\n"
            "Conversing with many people: Initiating, maintaining, shaping and terminating a dialogue or interchange with more than one individual, such as in starting and participating in a group interchange."
        )
    },
    "Discussion": {
        "definition": "Starting, sustaining and ending an examination of a matter, with arguments for or against, or debate carried out by means of spoken, written, sign or other forms of language, with one or more people one knows or who are strangers, in formal or casual settings.",
        "sub_activities": (
            "Discussion with one person: Initiating, maintaining, shaping or terminating an argument or debate with one person.\n"
            "Discussion with many people: Initiating, maintaining, shaping or terminating an argument or debate with more than one individual."
        )
    },
    "Using communication devices and techniques": {
        "definition": "Using devices, techniques and other means for the purposes of communicating.",
        "examples": "Calling a friend on the telephone; using typewriters, computers and Braille writers, as a means of communication; reading lips."
    }
},

    

"self-care": {
    "Washing oneself": {
        "definition": "Washing and drying one's whole body, or body parts.",
        "examples": "Using water and appropriate cleaning and drying materials or methods, such as bathing, showering, washing hands and feet, face and hair, and drying with a towel."
    },
    "Caring for body parts": {
        "definition": "Looking after those parts of the body (skin, face, teeth, scalp, nails and genitals) that require more than washing and drying.",
        "examples": (
            "Looking after the texture and hydration of one's skin, such as by removing calluses or corns and using moisturizing lotions or cosmetics;\n"
            "Looking after dental hygiene, such as by brushing teeth, flossing, and taking care of dental prosthesis or orthosis;\n"
            "Looking after the hair on the head and face, such as by combing, styling, shaving, or trimming;\n"
            "Cleaning, trimming or polishing the fingernails;\n"
            "Cleaning, trimming or polishing the toenails;\n"
            "Cleaning the nose and looking after nasal hygiene;\n"
            "Cleaning ears and looking after ear hygiene."
        )
    },
    "Toileting": {
        "definition": "Planning and carrying out the elimination of human waste (menstruation, urination and defecation), and cleaning oneself afterwards.",
        "sub_activities": (
            "Regulating urination: Coordinating and managing urination, such as by indicating need, getting into the proper position, choosing and getting to an appropriate place for urination, manipulating clothing before and after urination, and cleaning oneself after urination;\n"
            "Regulating defecation: Coordinating and managing defecation such as by indicating need, getting into the proper position, choosing and getting to an appropriate place for defecation, manipulating clothing before and after defecation, and cleaning oneself after defecation;\n"
            "Menstrual care: Coordinating, planning and caring for menstruation, such as by anticipating menstruation and using sanitary towels and napkins."
        )
    },
    "Dressing": {
        "definition": "Carrying out the coordinated actions and tasks of putting on and taking off clothes and footwear in sequence and in keeping with climatic and social conditions.",
        "examples": (
            "Putting on, adjusting and removing shirts, skirts, blouses, pants, undergarments, saris, kimono, tights, hats, gloves, coats, shoes, boots, sandals and slippers;\n"
            "Putting clothes on over the head, arms and shoulders, and on the lower and upper halves of the body;\n"
            "Putting on gloves and headgear;\n"
            "Taking clothes off over the head, arms and shoulders, and off the lower and upper halves of the body;\n"
            "Taking off gloves and headgear."
        ),
        "sub_activities": (
            "Putting on clothes: Carrying out the coordinated tasks of putting clothes on various parts of the body;\n"
            "Taking off clothes: Carrying out the coordinated tasks of taking clothes off various parts of the body;\n"
            "Putting on footwear: Carrying out the coordinated tasks of putting on socks, stockings and footwear;\n"
            "Taking off footwear: Carrying out the coordinated tasks of taking off socks, stockings and footwear;\n"
            "Choosing appropriate clothing: Following implicit or explicit dress codes and conventions of one's society or culture and dressing in keeping with climatic conditions."
        )
    },
    "Eating": {
        "definition": "Carrying out the coordinated tasks and actions of eating food that has been served, bringing it to the mouth and consuming it in culturally acceptable ways, cutting or breaking food into pieces, opening containers and packets, using eating implements, having meals, feasting or dining."
    },
    "Drinking": {
        "definition": "Taking hold of a drink, bringing it to the mouth, and consuming the drink in culturally acceptable ways, mixing, stirring and pouring liquids for drinking, opening bottles and cans, drinking through a straw or drinking running water such as from a tap or a spring; feeding or suckling from the breast."
    },
    "Looking after one's health": {
        "definition": "Ensuring physical comfort, health and physical and mental well-being.",
        "examples": (
            "Maintaining a balanced diet and an appropriate level of physical activity;\n"
            "Keeping warm or cool as necessary;\n"
            "Avoiding harms to health, such as following safe sex practices by using condoms;\n"
            "Getting immunizations and regular physical examinations."
        ),
        "sub_activities": (
            "Ensuring one's physical comfort: Caring for oneself by being aware that one needs to ensure, and ensuring, that one's body is in a comfortable position, that one is not feeling too hot, cold or wet, and that one has adequate lighting;\n"
            "Managing diet and fitness: Caring for oneself by being aware of the need and by selecting and consuming nutritious foods and maintaining physical fitness;\n"
            "Maintaining one's health: Caring for oneself by being aware of the need and doing what is required to look after one's health, both to respond to risks to health and to prevent ill-health, such as by seeking assistance (professional and non-professional), following medical and other health advice, and managing risks to health such as injuries, communicable diseases, drug-taking and sexually transmitted diseases."
        )
    }
}

}


save_pred_data(ICF_cate_comb, file_path_icf)



# save ICF function 

ICF_defs = {
 
    "mobility": "about moving by changing body position or location or by transferring from one place to another, by carrying, moving or manipulating objects, by walking, running or climbing, and by using various forms of transportation",

    "self-care": "about caring for oneself, washing and drying oneself, caring for one's body and body parts, dressing, eating and drinking, and looking after one's health",

    "communication": "about general and specific features of communicating by language, signs and symbols, including receiving and producing messages, carrying on conversations, and using communication devices and techniques"

            }

icf_def_file = "icf_def.json"
file_path_icf_def = os.path.join(dir_conver, icf_def_file)
save_pred_data(ICF_defs, file_path_icf_def)



# save examples

examples= {"mobility":{
                "function":["""When the given conversation history is: "C: Do you often go up and down stairs at home, Mrs. Richards? P: Yes, I do. I usually go up to my bedroom on the second floor.",
                        the following up questions on monitoring function level can be: "c: did you manage to walk the stairs today mrs Richards? P: yes I did, but in the morning my leg was hurting so it took some time to get done c: okay, did it get better during the day to walk the stairs p: yes in the afternoon it felt better."
                        """,
                       """When the given conversation history is: "C: How are you feeling today, Ms. Thompson? P: I'm feeling pretty good, thank you. C: Did you enjoy your daily walk with your walker? P: Yes, it was nice to get some fresh air and stretch my legs.",
                       the following up questions on monitoring function level can be: "c: did you use your walker when going to the park today mrs C? p: yes I went with my walker, because the path was a bit slippery due to the rain c:can walk as far as you want using the walker in the park. p: the walker enables me to walk as I want want with less energy."
                       """
                      ],
                "emotion":["""When the given conversation history is: "C: How are you feeling today? Have you been comfortable moving and changing body positions? P: Yes, I feel alright today. I use a chair with some extra cushions to help me get up easier.",
                       the following up questions on emotional feedback can be: "c: how do you feel about needing help to move around in your bed? P: at first I was bothered about it, but now it's fine. c: why were you bothered about it? P: I did not want to concern my husband in helping me turning in bed, but after he said he is happy to help me turning I don't feel upset about it anymore. c: okay, that's great. that also means that you husband is still phyically fit? P: yes he is actually and that gives me a reassuring feeling about being able to live at home with his support."
                       """,
                    """When the given conversation history is: "c: have you been able to get up from the couch last night? P: I am afraid I needed some assistance getting up from the couch last night. c: ah, that is not very nice than. How come you were not able to get up yourself? p: I fell asleep looking at the TV and when I wanted to go to the toilet I notice my back hurt and I could not get up by myself. c: and then what happened? p: I called for my husband who was in the other room and he supported my getting of the couch.",
                    the following up questions on emotional feedback can be: "c: how did you feel about not being able to get up from the couch? P: I felt stupid, because I know falling asleep in front of the TV often makes my back hurt. c: have you already thought of a sollution for that? p: I have been thinking in using pillows to support my back, but I keep foretting them. c: maybe talk about it with your husband then. if this prevents you from getting a sore back, you don't have to worry about asking for help getting up. p: that is a good idea!"
                    """,
                    ],
                       },
            "self-care":{
                "function":["""When the given conversation history is: "C: Good morning! How did dressing go for you this morning?

P: Oh, it took a bit longer than usual today, but I managed to get my favorite outfit on.
",
                        the following up questions on monitoring function level can be: "C: Oh, so you managed it without help?

P: Yes, I did

C: Why did it take more time than usual?

P: Because I wanted to wear a blouse with buttons

C: What's tricky about that?

P: I have trouble getting the buttons to close."
                        """,
                       """When the given conversation history is: "C: How have you been feeling today?

P: I've been doing well, thank you for asking.

C: Have you been keeping track of your meals and exercise routine?

P: Yes, I've been making sure to have my fruits and vegetables and go for a short walk each day.

",
                       the following up questions on monitoring function level can be: "c: Oh, that's very good of you! Do you do any other things for your health?

p: Yes, I make sure I have enough relaxation during the day

c: How do you relax best?

p: I prefer to lie down for half an hour with meditation music on

c: it sounds like you are very conscious of your health?

p: Yes, I find it very important."
                       """
                      ],
                "emotion":["""When the given conversation history is: "C: Good morning! How did dressing go for you this morning?

P: Oh, it took a bit longer than usual today, but I managed to get my favorite outfit on.",
                          the following up questions on emotional feedback can be: "c: How do you feel about that not working well anymore?

p: I find it difficult, but it's part of age. Fine motor skills are not what they used to be.

c: So it doesn't really bother you?

p: no, I just take more time for it, and don't wear a blouse with buttons every day."
                            """,
                          """When the given conversation history is: "C: How have you been feeling today?

P: I've been doing well, thank you for asking.

C: Have you been keeping track of your meals and exercise routine?

P: Yes, I've been making sure to have my fruits and vegetables and go for a short walk each day.

",
                            the following up questions on emotional feedback can be: "C:Is it important for you to take good care of yourself?

p: Yes, it makes me feel good."
                            """,
                          ],
            },
            "communication":{
                "function":["""When the given conversation history is: "C: Good morning! How are you feeling today?

P: Good morning. I'm feeling pretty good, thank you for asking.

C: I noticed you've been practicing formal sign language a lot lately. Are you enjoying the process?

P: Yes, I've been enjoying learning and communicating through sign language. It's challenging but rewarding.

C: That's great to hear. Is there a particular part of sign language that you find most interesting?

P: I find expressing emotions through sign language particularly fascinating. It adds depth to my conversations
",
                        the following up questions on monitoring function level can be: "C: How long do you practice on average?

P: I practice on average 30 minutes per day?

C: Do you also have conversations with people in sign language?

P: Yes I do,I can have a short conversation in sign language with others

C: That is great, how long have you been learning sign language now?

P: I have started 1 year ago."
                        """,
                       """When the given conversation history is: "C: How have you been enjoying reading the daily newspaper lately?

P: Oh, I've been spending some time each morning trying to catch up on current events.


C: That's great to hear! Is there a particular section you prefer reading first?

P: I always start with the headlines and then usually move on to the opinion pieces.

C: Sounds like a good routine. Have you come across any interesting articles recently?

P: Yes, I read a compelling piece on a local community initiative that caught my attention.
",
                       the following up questions on monitoring function level can be: "C: It sounds like you are very used to reading the newspaper, nice. Are there also other ways to keep up with the news?

P: Yes, every day I read news items on my computer as well

C; what sources do you use?

P: I read newsletter from various magazine every week that are sent by mail

C: How long does it take you to read the newsletter?

P: On average I read 1 hour a week newsletters

C: What do you prefer, receiving news events through  the newsletters or the newspapers?

P: I prefer to read the newspapers every day."
                       """
                      ],
                "emotion":["""When the given conversation history is: "C: Good morning! How are you feeling today?

P: Good morning. I'm feeling pretty good, thank you for asking.

C: I noticed you've been practicing formal sign language a lot lately. Are you enjoying the process?

P: Yes, I've been enjoying learning and communicating through sign language. It's challenging but rewarding.

C: That's great to hear. Is there a particular part of sign language that you find most interesting?

P: I find expressing emotions through sign language particularly fascinating. It adds depth to my conversations
",
                          the following up questions on emotional feedback can be: "C: You told me you like expressing emotions, can you tell me more about expressing emotions in sign language

P: Off course, for me it is really important that people feel included and through expressing emotions you can really have a meaningful conversation with others

C: How do you feel about learning to communicate with sign language?

P: I feel really proud that I was able to learn it, it was a lot of hard work

C: can you tell me more about the hard work learning sign language?

P: Well, you have to learn the gesture, which are a lot and off course you have to learn to communicate in a new way."
                          """,
                          """When the given conversation history is: "C: How have you been enjoying reading the daily newspaper lately?

P: Oh, I've been spending some time each morning trying to catch up on current events.


C: That's great to hear! Is there a particular section you prefer reading first?

P: I always start with the headlines and then usually move on to the opinion pieces.

C: Sounds like a good routine. Have you come across any interesting articles recently?

P: Yes, I read a compelling piece on a local community initiative that caught my attention.
",
                            the following up questions on emotional feedback can be: "C: It sounds like you really enjoy reading the newspapers. Can you tell me more about what you like about it?

P: I like to be connected to the world around me, it give me a good feeling to know I can still keep up with the news

C: What makes it so important for you?

P: Well, as you get older, your world becomes smaller. In this way I still feel part and I am proud I can still manage to read the newspapers 

C: And is it the same for the newsletters?

P: No, I enjoy reading the newsletters because in that way I am still connected to my old profession and I enjoy reading the latest developments in my field
"
                        """,
                            ],
            }


}
            
icf_example_file = "examples.json"
file_path_icf_def = os.path.join(dir_conver, icf_example_file)
save_pred_data(examples, file_path_icf_def)


