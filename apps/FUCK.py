#include <stdlib.h>	// for remove exit() warning
#include <unistd.h>
#include <sys/stat.h>
#include <sys/times.h>
#include <fcntl.h>
#include <signal.h>

#define BUF_SIZ 1024

int ccpid,cpid;
int _strlen(char* c){int i=0;while(c[i++]!='\0');return i-1;}
int _strcpy(char* d,char* o,int l)
{
	int i;
	for(i=0;i<l;i++)d[i]=o[i];
	return i;
}
int _strcmp(char* c1,char* c2,int len)
{
	int i;
	for(i=0;i<len;i++)
		if(c1[i]!=c2[i])
			return -1;
	return 0;
}
void prints(char *s){write(1,s,_strlen(s));}
int stoi(char *c)
{
	int i,num=0;
	for(i=0;i<_strlen(c);i++)
	{
		num*=10;
		num+=c[i]-'0';
	}
	return num;
}
void itos(int num,char *c_)
{
	int i,j;
	char c[10];
	for(i=0;i<10;i++)
	{
		c[i]='0'+num%10;
		num/=10;
		if(num==0)
			break;
	}
	for(j=0;j<=i;j++)
		c_[j]=c[i-j];
	c_[j]='\0';
}

void sigalrm_handler(int signo)
{
	static int elapsed_time=0;
	char buf[BUF_SIZ];
	if(elapsed_time!=0)
	{
		prints("\n\nProgram running over ");
		itos(elapsed_time,buf);
		prints(buf);
		prints("sec !\nDo you want to terminate this program?(y/n)");
		read(0,buf,BUF_SIZ);
		if(buf[0]=='y')
		{
			kill(ccpid,SIGKILL);
			kill(cpid,SIGKILL);
			exit(0);
		}
		prints("\n");
		getlogin_r(buf,BUF_SIZ);
		prints(buf);
		prints("@sbash:");
		getcwd(buf,BUF_SIZ);
		prints(buf);
		prints("$");
	}
	alarm(10);
	elapsed_time+=10;
}

int main(int argc,char** argv)
{
	char* arg[5]={"/usr/bin/gcc","-o"};
	char* env[]=
	{
		"HOME=/",
		"PATH=/bin:/usr/bin",
		"TZ=UTC0",
		0
	};
	struct stat statbuf;
	struct timeval tbuf1,tbuf2;
	mode_t file_mode;
	int size,flag,pid,fd,status,pipes[2];
	char buf[BUF_SIZ];
	prints("=======================================================\n");
	prints("Hello! This program check your C source's running time.\n");
	if(argc==1)
	{
		prints("Please put your C source's name as Argument.\n");
		prints(" e.g) ./program_name my_source.c\n");
		prints("=======================================================\n");
		exit(-1);
	}
	prints("=======================================================\n");
	flag=access(argv[1],F_OK);
	if(flag)
	{
		prints("Oops, this file doesn't exist!\n");
		exit(-1);
	}
	flag=access(argv[1],R_OK);
	if(flag)
	{
		prints("Oops, this file can't be read\n");
		exit(-1);
	}
	fd=open(argv[1],O_RDONLY);
	if(fstat(fd,&statbuf)==-1)
	{
		prints("fstat error\n");
		exit(-1);
	}
	close(fd);
	file_mode=statbuf.st_mode;
	if(!S_ISREG(file_mode))
	{
		prints("It's not Regular File!\n");
		exit(-1);
	}

	if(pipe(pipes)<0)
	{
		prints("pipe error\n");
		exit(-1);
	}

	pid=fork();
	if(pid==0)
	{
		int pipes2[2];
		char filename[_strlen(argv[1])-1];
		_strcpy(filename,argv[1],_strlen(argv[1])-2);
		filename[_strlen(argv[1])-2]='\0';
		pid=fork();
		if(pid==0)
		{
			arg[2]=sbrk(0);
			sbrk(sizeof(char)*(_strlen(argv[1])-1));
			_strcpy(arg[2],filename,_strlen(argv[1])-1);

			arg[3]=sbrk(0);
			sbrk(sizeof(char)*(_strlen(argv[1])+1));
			_strcpy(arg[3],argv[1],_strlen(argv[1])+1);
			execve(arg[0],arg,env);
		}
		wait(NULL);
		arg[2]=arg[3]=NULL;
		sbrk(-sizeof(char)*(_strlen(argv[1])-1));
		sbrk(-sizeof(char)*(_strlen(argv[1])+1));
		struct timespec timespec;
		timespec.tv_sec=0;
		timespec.tv_nsec=50000000;
		nanosleep(&timespec,NULL);
		flag=access(filename,F_OK);
		if(flag)
		{
			prints("Oops, Compilation Failure !\n");
			kill(getppid(),SIGKILL);
			exit(-1);
		}
		char *sarg[2];
		sarg[0]=sbrk(0);
		sbrk(sizeof(char)*(_strlen(filename)+1));
		_strcpy(sarg[0],filename,_strlen(filename));
		sarg[_strlen(filename)]='\0';
		sarg[1]=NULL;
		sarg[2]=sbrk(0);
		sbrk(sizeof(char)*(_strlen(filename)+8));
		int l=_strcpy(sarg[2],filename,_strlen(filename));
		sarg[2][l++]='.';sarg[2][l++]='o';sarg[2][l++]='u';
		sarg[2][l++]='t';sarg[2][l++]='p';sarg[2][l++]='u';
		sarg[2][l++]='t';sarg[2][l++]='\0';
		creat(sarg[2],0644);
		int fout=open(sarg[2],O_RDWR);
		if(pipe(pipes2)<0)
		{
			prints("pipe error\n");
			exit(-1);
		}
		gettimeofday(&tbuf1,NULL);
		pid=fork();
		if(pid==0)
		{
			char pid_[10];
			itos(getpid(),pid_);
			pid_[_strlen(pid_)+1]='\n';
			write(pipes2[1],pid_,_strlen(pid_)+2);
			dup2(fout,1);
			dup2(fout,2);
			prints("Program \"");
			prints(filename);
			prints("\" Started !\n");
			execve(filename,sarg,env);
		}
		read(pipes2[0],buf,BUF_SIZ);
		kill(getppid(),SIGALRM);
		write(pipes[1],buf,BUF_SIZ);
		waitpid(stoi(buf),&status,0);
		gettimeofday(&tbuf2,NULL);
		sarg[0]=NULL;
		sbrk(-sizeof(char)*_strlen(filename+1));
		prints("elapsed time (user) : ");
		int sec=tbuf2.tv_sec-tbuf1.tv_sec;
		int usec=tbuf2.tv_usec-tbuf1.tv_usec;
		if(usec<0){sec--;usec+=1000000;}
		itos(sec,buf);
		write(1,buf,_strlen(buf));
		prints(".");
		int i,j=100000;
		for(i=0;i<6;i++)
		{
			if(usec/j==0){prints("0");j/=10;}
			else break;
		}
		itos(usec,buf);
		write(1,buf,_strlen(buf));
		prints("s\n");
		exit(0);
	}
	char user_id[32];
	getlogin_r(user_id,32);
	signal(SIGALRM,sigalrm_handler);
	read(pipes[0],buf,BUF_SIZ);
	ccpid=stoi(buf);
	cpid=pid;
	sleep(1);
	prints("\n* You can use simple shell until program end !\n");
	prints("* This simple shell support below commands !\n");
	prints(" > Commands : cd, ls, mkdir, rmdir, mv(only renaming)\n\n");
	while(1)
	{
		prints(user_id);
		prints("@sbash:");
		getcwd(buf,BUF_SIZ);
		prints(buf);
		prints("$");
		size=read(0,buf,BUF_SIZ);
		if(_strcmp(buf,"ls",2)==0)
		{
			char* a[3]={"/bin/ls","-p",NULL};
			pid=fork();
			if(pid==0)
				execve("/bin/ls",a,env);
			wait(NULL);
		}
		else if(_strcmp(buf,"cd",2)==0)
		{
			int i;
			for(i=0;i<size-4;i++)
				buf[i]=buf[i+3];
			buf[i]='\0';
			chdir(buf);
		}
		else if(_strcmp(buf,"mkdir",5)==0)
		{
			int i;
			for(i=0;i<size-7;i++)
				buf[i]=buf[i+6];
			buf[i]='\0';
			mkdir(buf,S_IRWXU);
		}
		else if(_strcmp(buf,"rmdir",5)==0)
		{
			int i;
			for(i=0;i<size-7;i++)
				buf[i]=buf[i+6];
			buf[i]='\0';
			rmdir(buf);
		}
		else if(_strcmp(buf,"mv",2)==0)
		{
			int i,j,idx=0;
			char orig[BUF_SIZ];
			char dest[BUF_SIZ];
			for(i=0;i<size-1;i++)
			{
				if(buf[i]==' ')
				{
					if(idx==1)
						orig[j]='\0';
					idx++;
					j=0;
					continue;
				}
				if(idx==1)
					orig[j++]=buf[i];
				if(idx==2)
					dest[j++]=buf[i];
			}
			dest[j]='\0';
			rename(orig,dest);
		}
	}
	wait(NULL);
}
