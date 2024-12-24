#include <pistache/endpoint.h>
#include <pistache/http.h>
#include <cstdlib>

using namespace Pistache;

// See https://pistacheio.github.io/pistache/docs/routing

struct SimHandler : public Http::Handler {
  HTTP_PROTOTYPE(SimHandler)

  void onRequest(const Http::Request& request, Http::ResponseWriter response) override {
    response.headers().add<Http::Header::AccessControlAllowOrigin>("*");
    response.headers().add<Http::Header::AccessControlAllowMethods>("POST");
    response.headers().add<Http::Header::AccessControlAllowHeaders>("Content-Type");
    
    if (request.method() == Http::Method::Post) {
      std::cout << "Received POST Request" << std::endl;
      system("$PYTHON_VENV /projects/simulator/python_facade/spawn_simulation.py");
      response.send(Http::Code::Ok);
    } 
    else {
      std::cout << "Received Not Allowed Request" << std::endl;
      response.send(Http::Code::Method_Not_Allowed);
    }
  }
};

int main() {
  Http::listenAndServe<SimHandler>(Pistache::Address("*:8080"));
}
