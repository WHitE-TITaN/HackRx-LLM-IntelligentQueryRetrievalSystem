import java.io.IOException;
import java.io.PrintWriter;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@WebServlet("/hackrx/run")
public class requestHandler extends HttpServlet {
  @Override
    protected  void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
    {
      PrintWriter out = response.getWriter();
      RequestDispatcher dispatch = request.getRequestDispatcher("error.jsp");
      response.setContentType("text/html");

      out.println("<h1>Bad Request</h1>");
      dispatch.include(request, response);
    }

  @Override
    protected void doPost(HttpServletRequest Request, HttpServletResponse Response) throws IOException, ServletException
    {
      try{

        HttpClient client = HttpClient.newHttpClient();
        String jsonQuery = """
        {
          "documents": "https://drive.google.com/uc?export=download&id=1AJStH_SArQdomXZoaygD9GEWlShnLaBp",
          "key": "**********",
          "question": [
                      "what is the Address of the company?,
                      "what is the contact number of the company?",
                      "what is the email address of the company?",
                      "what is the website of the company?"
                      ]
        }
        """;

        HttpRequest request = HttpRequest.newBuilder()
          .uri(URI.create("https://hackrx-llm.onrender.com/process"))
          .header("Content-Type", "application/json")
          .POST(HttpRequest.BodyPublishers.ofString(jsonQuery)) 
          .build();
        
        HttpResponse<String> httpResponse = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Response Code: " + httpResponse.statusCode());
        System.out.println("Response Body: " + httpResponse.body());

        PrintWriter out = Response.getWriter();
        Response.setContentType("text/html");
        out.println("<h1>Response from HackRx</h1>");
        out.println("<pre>" + httpResponse.body() + "</pre>");
        
      }
      catch(Exception e){
        PrintWriter out = Response.getWriter();
        RequestDispatcher dispatch = Request.getRequestDispatcher("error.jsp");
        Response.setContentType("text/html");

        out.println("<h1>Internal Server Error</h1>");
        dispatch.include(Request, Response);

        e.printStackTrace(out);
      }
    }
}
