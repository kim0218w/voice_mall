import sub.work_flow as wf

def main():
    # 작업 흐름 제어 하는 객체
    wf_ctr = wf.controller()
    while True:
        
        try:
            stage_func = wf_ctr.recognize_voice_interface()
            stage_func()
        except Exception as e:
            print(e)
        

if __name__ == '__main__':
    main()
   



