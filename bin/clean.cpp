#include<iostream>
#include <stdio.h>  
#include <iostream>  
#include <string>  
#include <vector>  
#include <fstream>  
#include <sstream>  
#include <math.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <dirent.h>  
#include <unistd.h>  
#include <string.h> 
using namespace std;  

class eMyRect2D
{
    public:
        double minx;
        double miny;
        double maxx;
        double maxy;
    public:
        eMyRect2D(){
            minx=miny=maxx=maxy=0;
        }
        eMyRect2D(double _minx,double _miny,double _maxx,double _maxy){
            minx = _minx;
            miny = _miny;
            maxx = _maxx;
            maxy = _maxy;
        }
        bool Contains(double x,double y)const{
            return !(minx > x || maxx < x || 
                miny > y || maxy < y);
        }
        void print(){
            cout << minx << "," << miny << "," << maxx << "," << maxy<< endl;
        }

};

class Util
{
     const double EARTH_RADIUS = 6378137;
     const double RAD = M_PI / 180.0;

    /// <summary>
    /// 根据提供的经度和纬度、以及半径，取得此半径内的最大最小经纬度
    /// </summary>
    /// <param name="lat">纬度</param>
    /// <param name="lon">经度</param>
    /// <param name="raidus">半径(米)</param>
    /// <returns></returns>
public:
    static void GetBound(double lat, double lon, int raidus,eMyRect2D& rect)
    {

        double latitude = lat;
        double longitude = lon;

        double degree = (24901 * 1609) / 360.0;
        double raidusMile = raidus;

        double dpmLat = 1 / degree;
        double radiusLat = dpmLat * raidusMile;
        double minLat = latitude - radiusLat;
        double maxLat = latitude + radiusLat;

        double mpdLng = degree * cos(latitude * (M_PI / 180));
        double dpmLng = 1 / mpdLng;
        double radiusLng = dpmLng * raidusMile;
        double minLng = longitude - radiusLng;
        double maxLng = longitude + radiusLng;
        rect.minx = minLng;
        rect.miny = minLat;
        rect.maxx = maxLng;
        rect.maxy = maxLat;

    }

    static vector<string> split(string strtem,char a)  
    {  
        vector<string> strvec;  
  
        string::size_type pos1, pos2;  
        pos2 = strtem.find(a);  
        pos1 = 0;  
        while (string::npos != pos2)  
        {  
            strvec.push_back(strtem.substr(pos1, pos2 - pos1));  

            pos1 = pos2 + 1;  
            pos2 = strtem.find(a, pos1);  
        }  
        strvec.push_back(strtem.substr(pos1));  
        return strvec;  
    }  
};
  
int main(int arg,char *args[])  
{  
    if(arg<2)
        return 1;
        
    vector<eMyRect2D> _rects;

    // 读文件  
    ifstream inFile("液厂84坐标.csv", ios::in);  
    string lineStr;  
    while (getline(inFile, lineStr)) 
    {
        vector<string> coors = Util::split(lineStr,',');

        eMyRect2D rt;
        Util::GetBound(atof(coors[1].c_str()),atof(coors[2].c_str()),1000,rt);
        _rects.push_back(rt);
    } 
    inFile.close();

    {  
       DIR* dp;  
       struct dirent* dirp;  
       dp = opendir(args[1]);  
       if(dp == NULL)  
       {  
          printf("open error ");  
          return 0;  
       }  
       while((dirp = readdir(dp)) != NULL )  
       {  
           if(strcmp( dirp->d_name , "." ) == 0 || strcmp( dirp->d_name , "..") == 0)  
                continue;  
           
            // 写文件  
            ofstream outFile;  
            char new_name[256];
            //strcpy(new_name,"/data/030/Data_11/YuanShiData_11/");
	    strcpy(new_name,args[1]);

            strcat(new_name,dirp->d_name);
            // 读车辆信息文件  
            ifstream carFile(new_name, ios::in);
            //strcat(new_name,".csv");
            //printf(new_name);
             
	    char out_name[256];
	        strcpy(out_name,args[2]);
//            strcpy(out_name,"/data/030/Data_09/YuanShiData/");
	    strcat(out_name,dirp->d_name);
	   
            outFile.open(out_name, ios::out);

            while (getline(carFile, lineStr)) 
            {
                vector<string> line = Util::split(lineStr,',');
                //cout << atof(line[9].c_str())/1000000 <<"," <<atof(line[10].c_str())/1000000 << endl; 

                for (vector<eMyRect2D>::const_iterator iter = _rects.begin(); iter != _rects.end(); iter++)
                {
                    eMyRect2D rt=(*iter);
                    if(rt.Contains(atof(line[9].c_str())/1000000,atof(line[10].c_str())/1000000))
                        outFile << lineStr << endl; 
                }
            }
            outFile.close();
       }  
       closedir(dp);
    }  

    //getchar(); 
    return 0;  
}
