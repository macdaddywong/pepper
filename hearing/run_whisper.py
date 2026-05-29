# run_whisper.py
from hearing import Hearing




ears = Hearing()

if __name__ == "__main__":
    # use_microphone = input("Use microphone?")
    # use_microphone = use_microphone.lower().strip()
    # if use_microphone not in ['y', 'yes', "use", "use_microphone", "use microphone"]:
    #     exit(0)
        
    ears.turn_on_microphone()
    text = ears.wav_breakdown()
    print(f"We were returned this as text:")
    print("\n\t\u2022RAW:", text)
    print("\n\t\u2022CLEAN:", ears.clean(text))
    n = input("valid? (Y/N) ")
    
    if n.lower().strip() not in ['y', 'yes']:
        exit(0) 
    
    

