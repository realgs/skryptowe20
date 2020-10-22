#include <string>

int main(int argc, char *argv[]) {

    if (argc > 4)
        return 1;
    for (int i = 0; i < argc; i++) {
        if (atoi(argv[i]) > 4)
            return 2;
    }

    return 0;
}