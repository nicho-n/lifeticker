#include <sys/mman.h>
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <cstring>
#include <cstdlib>
#include <vector>
using namespace std;

size_t filesize(int fd){
        return lseek(fd, 0, SEEK_END);
}

size_t totalFilesize(vector<int> fds, int start, int end){
	size_t total = 0;
	for (int i = start; i < end; i++)
		total += filesize(fds[i]);
	return total;
}

int main(int argc, char **argv){
	vector<int> fds; int n = 0; int fd; int fd_out; int c;
	char * out_filename = argv[argc-1];

	fd_out = open(out_filename, O_RDWR | O_CREAT | O_EXCL, 0777);
	if (fd_out == -1){
		cout << "File exists! Quitting.." << endl;
		return 0;
	}

	for (int i=1; i<argc-1; i++){
		if ((fd = open(argv[i], O_RDONLY)) == -1)
			perror(argv[i]);
		else
			fds.push_back(fd);
	}

	int total_size = totalFilesize(fds, 0, fds.size());

	void * dest = mmap(NULL, total_size, PROT_WRITE, MAP_SHARED, fd_out, 0);
	ftruncate(fd_out, total_size);

	for (int i = 0; i < fds.size(); i++){
		size_t sz = filesize(fds[i]);
		void * src = mmap(NULL, sz, PROT_READ, MAP_PRIVATE, fds[i], 0);
		madvise(src, sz, MADV_SEQUENTIAL);
		memcpy((dest + n), src, sz);
		n += sz;
	}

	return 0;
}
