#include <iostream>



int main(int argc, char* argv[]) {
	bool isSilent = false;
	std::string silence = argv[1];
	int argument_amount = 2;
	if(argc > 1 && silence == "/s" || silence == "/S"){
		isSilent = true;
		argument_amount++;
	}
	if(argc == argument_amount){
		if(!isSilent){
			printf("Return code: 11");
		}
		return 11;
	}
	if(argc > argument_amount){
		if(!isSilent){
			printf("Return code: 13");
		}
		return 13;
	}
	if(argc == argument_amount){
		for(int i = 0; i < argument_amount; i++){
			if(argv[i] != "/s" && argv[i] != "/S" && isdigit(*argv[i]) ){
				int rc = int(*argv[1]) - 48;
				if(!isSilent){
					printf("Return code: %i", rc);
				}
				return rc;
			} else if(argv[i] != "/s" && argv[i] != "/S" && !isdigit(*argv[i])){
				if(!isSilent){
					printf("Return code: 12");
				}
				return 12;
			}
		}
	}

}
