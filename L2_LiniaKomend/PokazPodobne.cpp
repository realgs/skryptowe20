#include <iostream>
#include <cctype>

#define DELIMETER ";"

int main(int argc, char** argv, char** envp) {
    bool b_found = false;
    bool b_is_silent = false;
    std::string s_message = "";

    for (int i = 1; i < argc; ++i) {
        std::string s_wanted = argv[i];
        std::transform(s_wanted.begin(), s_wanted.end(),s_wanted.begin(), ::toupper);

        if (strcmp(s_wanted.c_str(), "/S") == 0) {
            b_is_silent = true;
        } else {
            for (int i = 0; envp[i] != nullptr; ++i) {
                std::string s(envp[i]);
                std::string s_name = s.substr(0, s.find('='));
                if (s_name.find(s_wanted) != std::string::npos) {
                    s_message += s_name;
                    s_message += "\n=\n";

                    std::string s_value = s.substr(s.find('='));
                    s_value.erase(0, 1);
                    int i_pos;
                    while ((i_pos = s_value.find(DELIMETER)) != std::string::npos) {
                        s_message += s_value.substr(0, i_pos);
                        s_message += "\n";
                        s_value.erase(0, i_pos + std::string(DELIMETER).length());
                    }
                    s_message += s_value.substr(0, i_pos);
                    s_message += "\n\n";

                    b_found = true;
                }
            }
            if (!b_found && !b_is_silent) {
                s_message += s_wanted;
                s_message += " = NONE\n";
            } else {
                b_found = false;
            }
        }
    }

    std::cout << s_message;
}
