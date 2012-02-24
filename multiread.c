// Does a linescan when called with 
// linescan2 steps range 
#define X_IDENT 1
#define Y_IDENT 0

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <comedilib.h>
#include "examples.h"
#include "common.c"
#include <time.h>

#define VERBOSE 0

#define ACQUIRE_CONTROL_OF_SEM 1
#define RELEASE_CONTROL_OF_SEM 0

int steps=101;
float startv=-5;
float stopv=5;
//float range=10;
float daqcal=0.953; // conversion of read voltage to read voltage
//const double aspectRatioFactor=1;
double start_tick;

void write_data(comedi_t * device, double voltage,int channel);

int controlSEM(comedi_t *device, int onOff);

char * getFullPath();
char * getFullPathForServer();
double waittime = 1e4; // 1 second

int main(int argc, char *argv[])
{

	printf(argv[0]);
	printf("\n");
	waittime=atof(argv[1])*1e6;
/*	steps=atoi(argv[3]);
	if (steps < 3) {
		steps=3;
	}
	startv=atof(argv[1]);
	stopv=atof(argv[2]);
	waittime=atof(argv[3]);
	printf("start at %f V\n", startv);
	printf("end at %f V\n", stopv);
	printf("# of steps is %d\n", steps);*/
	double voltage;
	comedi_t *device = comedi_open("/dev/comedi0");
	//printf("enter voltage ");
	//scanf("%lf", &voltage);
	int analogInSubdev=0;

	int dataIn;
	float input;
	float nowtime;
	int x_ind,y_ind;
	//int steps=1000;
	FILE *fp;
	
	fp = fopen(getFullPathForServer(), "w");

	char ch;
//	printf("Initializing DAQ and waiting\n");
//	write_data(device, startv,Y_IDENT);
	start_tick=clock();
//       while ( clock() - start_tick < waittime )
//               ; // do nothing but loop...


	printf("Reading many points \n");
//	for (x_ind=steps;x_ind>0;x_ind--)
//	{
//		voltage =  ((double)x_ind/(double)steps) * 20.0 -10.0;
//		write_data(device, voltage,X_IDENT);
		while ( clock() - start_tick < waittime )
		{
//			voltage = ((double)(y_ind)/((double)steps-1)) * (stopv-startv) +startv;
		//	write_data(device, voltage,Y_IDENT);
			//grab data 
		  comedi_data_read(device,analogInSubdev,0/*channel*/,0/*range*/,AREF_GROUND, &dataIn);
//			nowtime = clock() - start_tick;
			input=(dataIn/3276.6-10)/daqcal;

			fprintf(fp,"%f\n", input);
			//printf("dataIn %i\n",dataIn);
			//put data into a file	
		}
//		fprintf(fp,"\n");
//	}

//	close(fp);

	printf("done. \n");
	return 0;
}

/*  
void write_data(comedi_t * device, double voltage,int channel){
  int subdevice = 1;
  //int channel = 1;
  int range = 0;
  int analogref = AREF_GROUND;
  lsampl_t write_data;
  int ret;
  int data;
  data = (int) ((voltage + 10) * 3276.6);
  if (data > 0xffff)
  {
    data = 0xffff;
  }
  if (data < 0)
  {
    data = 0x0;
  }
  write_data = data;
  ret = comedi_data_write(device, subdevice, channel, range, analogref, write_data);
  if (ret < 0)
  {
    printf ("\nwrite_data(comedi_t * device, double voltage) function failed\n");
  }
}
*/

char* getFullPath()
{
	char * fullPath;
	char * home;
	char * fileName;
	home = getenv ("HOME");
	//printf(home);
	//printf("\n");
	fileName = "/data.dat";
	//printf(fileName);
	//printf("\n");

  fullPath = (char *)calloc(strlen(home) + strlen(fileName) + 1, sizeof(char));
	//fullPath = (char *)malloc((strlen(home) + strlen(fileName) + 1) *sizeof(char)); 

  strcat(fullPath, home);
  strcat(fullPath, fileName);


	printf("The file will go to :");
	printf(fullPath);
	printf("\n");
  return fullPath;
	//char *dir="/home/georgegdc/data_test.dat";
}

char* getFullPathForServer()
{
	char * fullPath;
	char * home;
	char * dir;
	char * fileName;
	home = "www-data"; //getenv ("USER");
	printf(">");
	printf(home);
	printf("<\n");

	//printf(home);
	//printf("\n");
	dir = "/tmp/";
	fileName = ".dat";
	//printf(fileName);
	//printf("\n");

  fullPath = (char *)calloc(strlen(home) + strlen(fileName) + strlen(dir) + 1, sizeof(char));
	//fullPath = (char *)malloc((strlen(home) + strlen(fileName) + 1) *sizeof(char)); 

  strcat(fullPath, dir);
  strcat(fullPath, home);
  strcat(fullPath, fileName);


	printf("The file will go to :");
	printf(fullPath);
	printf("\n");
  return fullPath;
	//char *dir="/home/georgegdc/data_test.dat";
}



  

