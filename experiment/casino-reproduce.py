import subprocess
import d4j_avatar
import d4j_fixminer
import d4j_kpar
import d4j_tbar
import getopt
import seeds

def main(argv):
    opts,args=getopt.getopt(argv,"",['finish-correct-patch','timeout=','max-iter='])
    if len(args)<5:
        print("Usage: python3 casino-reproduce.py [options] <project> <output_dir> <casino|original|seapr> <tool> <project_path> [seed]")
        exit(1)
    
    finish_correct_patch=False
    timeout=0
    max_iter=0
    for a,o in opts:
        if a=='--finish-correct-patch':
            finish_correct_patch=True
        elif a=='--timeout':
            timeout=int(o)
        elif a=='--max-iter':
            max_iter=int(o)

    project=args[0]
    output_dir=args[1]
    mode=args[2]
    tool=args[3]
    project_path=args[4]
    seed=-1
    if len(args)>5:
        seed=int(args[5])

    correct_dict=dict()
    with open(f'correct-{tool}.csv') as f:
        lines=f.readlines()
        for line in lines:
            line=line.strip()
            elem=line.split(',')

            cor_str=''
            for e in elem[1:]:
                cor_str+=e+','
            cor_str=cor_str[:-1]
            correct_dict[elem[0]]=cor_str

    if mode=='casino':
        if tool=='avatar' or tool=='fixminer' or tool=='kpar' or tool=='tbar':
            cmd=['python3','../casino.py','-o',output_dir,'-m','guided',"--use-exp-alpha",
                    '--tbar-mode','-w',f'{tool}/d4j/{project}/0' if tool=='fixminer' else f'{tool}/d4j/{project}','-t','180000','--use-pass-test']
            if project in correct_dict:
                cmd.append('-c')
                cmd.append(correct_dict[project])
            if seed!=-1:
                cmd.append('--seed')
                cmd.append(str(seed))
            else:
                cmd.append('--seed')
                cmd.append('0')
            if tool=='fixminer':
                cmd.append('--fixminer-mode')
            if finish_correct_patch:
                cmd.append('--finish-correct-patch')
            if timeout>0:
                cmd.append('-T')
                cmd.append(str(timeout))
            if max_iter>0:
                cmd.append('-E')
                cmd.append(str(max_iter))
            result=subprocess.run(cmd+['--','python3','../script/d4j_run_test.py',project_path])
    
    elif mode=='original':
        if tool=='avatar' or tool=='fixminer' or tool=='kpar' or tool=='tbar':
            cmd=['python3','../casino.py','-o',output_dir,'-m','tbar',"--use-exp-alpha",
                    '--tbar-mode','-w',f'{tool}/d4j/{project}/0' if tool=='fixminer' else f'{tool}/d4j/{project}','-t','180000','--use-pass-test']
            if project in correct_dict:
                cmd.append('-c')
                cmd.append(correct_dict[project])
            if tool=='fixminer':
                cmd.append('--fixminer-mode')
            if finish_correct_patch:
                cmd.append('--finish-correct-patch')
            if timeout>0:
                cmd.append('-T')
                cmd.append(str(timeout))
            if max_iter>0:
                cmd.append('-E')
                cmd.append(str(max_iter))
            result=subprocess.run(cmd+['--','python3','../script/d4j_run_test.py',project_path])

    elif mode=='seapr':
        if tool=='avatar' or tool=='fixminer' or tool=='kpar' or tool=='tbar':
            cmd=['python3','../casino.py','-o',output_dir,'-m','seapr',"--use-exp-alpha",'--use-pattern','--ignore-compile-error',
                    '--tbar-mode','-w',f'{tool}/d4j/{project}/0' if tool=='fixminer' else f'{tool}/d4j/{project}','-t','180000','--use-pass-test']
            if project in correct_dict:
                cmd.append('-c')
                cmd.append(correct_dict[project])
            if tool=='fixminer':
                cmd.append('--fixminer-mode')
            if finish_correct_patch:
                cmd.append('--finish-correct-patch')
            if timeout>0:
                cmd.append('-T')
                cmd.append(str(timeout))
            if max_iter>0:
                cmd.append('-E')
                cmd.append(str(max_iter))
            result=subprocess.run(cmd+['--','python3','../script/d4j_run_test.py',project_path])
