#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <ctime>
#include <stdlib.h>

using namespace std;

typedef vector<vector<char>> matrix;

//define variables
int height; //rows
int width; //columns
int attempt=1;

//define matrices
matrix cover;
matrix minefield;

void displayMinefield(int drow, int dcol)
{

  for (int i=0; i<=drow-1; i++)
  {
  for (int j=0; j<=dcol-1; j++)
  {
    if(cover[i][j]== '#' || cover[i][j]== '-' || cover[i][j]== 'F')
    cout<<cover[i][j]<<" ";
    else 
    {
    cout<<minefield[i][j]<<" ";
    }
    
  }
  cout <<endl;
  }
  cout <<endl;
}

  
void addMines (int minesRemaining)
  {
    
    //Generate random locations for the mine planting
    do 
    {
      int addRow = rand() % height;
      int addCol = rand() % width;
    
      if (minefield[addRow][addCol]!='*')
      {
       minefield[addRow][addCol]='*';
      }
      else
      {
      while(minefield[addRow][addCol]!='-')
      minefield[addRow][addCol]++;
      }
      minesRemaining--;
    }
    while (minesRemaining>0);
    
    cout<<"All mines added"<<endl;
  }


bool isMine (int mrow, int mcol)
  {
    if (cover[mrow-1][mcol-1]=='#' && minefield[mrow-1][mcol-1]=='*'){
      cover[mrow-1][mcol-1]=='*';
      displayMinefield(height, width);
      return true;
  }
  else
  {
    cover[mrow-1][mcol-1]='-';
    return false;
  }
    
  }

 
/*bool findBlanks(int brow, int bcol)
{
	//reveal the location
	cover[brow-1][bcol-1] = '-';

	if(minefield[brow-1][bcol-1] == '-')
	{
		queue<pair<int, int> > openLocations;
		openLocations.push(make_pair(brow-1, bcol-1));

		while(!openLocations.empty())
		{
			//Get the next location from our queue
			pair<int, int> next = openLocations.front();
			for(int dy = next.first-1; dy <= next.first+1; dy++)
			{
				for(int dx = next.second-1; dx <= next.second+1; dx++)
				{
					
					if(dy >= 0 && dy < height && dx >= 0 && dx < width)
					{
						//if this neighbor is a '-' location and hasn't
						//previously been revealed, add it to our list
						if(minefield[dy][dx] == '-' && cover[dy][dx] == '#')
							openLocations.push(make_pair(dy, dx));
						else
						{
						  
						}
					}
					}
			}
			cover[next.first][next.second] = '-';
			openLocations.pop();
		}
		return true;
	}
	else
	{
  cout<<"Failure in finding blank squares"<<endl;
  return false;
	}
}*/

bool findBlanks(int brow, int bcol)
{
  cover[brow-1][bcol-1] == '-';
  queue<pair<int, int> > openLocations;
	openLocations.push(make_pair(brow-1, bcol-1));
	pair<int, int> next; 
while (!openLocations.empty())
 {
   
  next = openLocations.front();
			for(int dy = next.first-1; dy <= next.first+1; dy++)
			{
			  for(int dx = next.second-1; dx <= next.second+1; dx++)
				{
				  if (dy >= 0 && dy < height && dx >= 0 && dx < width)
					{
						//if this neighbor is a '-' location and hasn't
						//previously been revealed, add it to our list
						if (cover[dy][dx]=='#' && minefield[dy][dx]== '-' )
						{
						  continue;
						}
						else
						{
						  if (cover[dy][dx]== '#')
						  {
						    cover[next.first][next.second]= '1';
						  }
						  else
						  {
						  
						  int isThere = (int)cover[next.first][next.second];
						  isThere++;
						  char buffer;
						  buffer = (char)isThere;
						  cout << buffer<< endl;
						  cover[next.first][next.second] = buffer;
						  }
						  }
						  
						}
					}
					}
					  
	cover [next.first][next.second]= '-';
	openLocations.pop();	
	}
			
  return true;
}


string flagMines(string flagvalue)
{
  int hflag;
  int vflag;
if ((flagvalue[0] == 'y' || flagvalue[0] == 'Y') && flagvalue.size() == 1 )
    {
      cout<<"Enter the row from 1 to "<<height<<" in which you want to flag: "<<endl;
      std::cin >> vflag;
      cout<<"Enter column from 1 to "<<width<<" in which you want to flag: "<<endl;
      std::cin >> hflag;
      if (cover[vflag-1][hflag-1]== '#')
  {
    cover[vflag-1][hflag-1]= 'F';
    return "Mine flagged successfully";
  }
  else 
  {
    return "Can't flag the location";
  }

    }
else if ((flagvalue[0] == 'n' || flagvalue[0] == 'N') && flagvalue.size() == 1)
    {
      return "No problem";
    }
else 
{
  return "Error occurred!!.";
}
}


string playthegame(int attempt)
{ 

do
{
  cout << "\n #Attempt: "<<attempt<< endl;
   
  //DISPLAY MINEFIELD
  displayMinefield(height, width);

 //Take entry from user
 int hentry;
 int ventry;
  cout << "Please enter your vertical entry from 1 to "<< height <<" to play: "<<endl;
  cin >> ventry;
  cout << "Please enter your horizontal entry from 1 to "<< width <<" to play: "<<endl;
  cin >> hentry;
  
//check for mine at the entry location  
  if (attempt!=1)
  {
  if (ventry<= height &&  hentry<=width )
  {
  if (isMine(ventry, hentry)== true)
  {
    displayMinefield(height, width);
    return "You stepped on a mine!! Game Over!!";
    break;
  }
  else
  {
    cout<<"You are safe!!"<<endl;
    bool blanks = findBlanks(ventry, hentry);
    displayMinefield(height, width);
    
    //Flag mines
    cout<<"Do you want to flag mines? Type 'y' or 'n': "<<endl;
      string flag;
      cin >> flag;
      //cout <<"Great!!"<<endl;
      string flagstatus = flagMines(flag);
      cout <<flagstatus<<endl;
   
    
  }
  }
  
  else {
    cout <<"Invalid entry!! Please try again."<<endl;
    string again= playthegame(attempt);
    cout <<again<<endl;
    
  }
  }
  
  
//attempt==1
  else
  {
      //1st attempt always blank
     if (ventry<= height &&  hentry<=width )
  { 
    if (isMine(ventry, hentry)== true)
    {
      minefield[ventry-1][hentry-1] = '-';
      int vblank, hblank =0;
      while (minefield[vblank][hblank]!='-' && hblank<width)
      {
        hblank++;
      }
      minefield[vblank][hblank] ='*'; //shift the mine to a new entry
      cover[vblank][hblank]= '#';
      cout<<"First attempt blank"<<endl;
      
    }
    else
    {
      cout <<"Not a mine!!Hurrahh!!"<<endl;
    }
  } 
  else
  {
    cout <<"Invalid entry!! Please try again."<<endl;
    string yetagain= playthegame(attempt);
    cout <<yetagain<<endl;
  }
  }

}
while(attempt++);
return "Congratulations!! You have successfully located all mines!!";
}


int main()
{
//Define variables
int no_of_mines;

  cout << "Please enter the height of your minefield: ";
  cin >> height;
  cout << "Please enter the width of your minefield: ";
  cin >> width;
  cout << "Please enter the no of mines of your minefield: ";
  cin >> no_of_mines;
  
//define cover
for(int i=0; i<height;i++)
{
   cover.push_back(vector<char>(width, '#'));
}

//FILL MINEFIELD
for(int i=0; i<height;i++)
  {
  minefield.push_back(vector<char>(width,'-'));
  }
  
//Add mines
addMines(no_of_mines);


//****PLAY THE GAME****//
string game = playthegame(1);
cout << game << endl;
  
  //Deallocate memory
  for(int i = 0; i < height; ++i)
   delete[] &cover[i];
delete[] &cover;

for(int i = 0; i < height; ++i)
   delete[] &minefield[i];
delete[] &minefield;
  
  return 0;
}
  

  
  
  
  