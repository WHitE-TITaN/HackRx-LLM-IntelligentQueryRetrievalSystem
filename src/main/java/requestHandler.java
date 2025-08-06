

import java.io.BufferedReader;
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

import org.json.JSONObject;

import application.authentication;

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

        StringBuilder sb = new StringBuilder();
        String line;
        BufferedReader reader = Request.getReader();

        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        
        String body = sb.toString().trim();
        if (body.isEmpty()) {
            PrintWriter out = Response.getWriter();
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Empty JSON body");

            Response.setContentType("application/json");
            Response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            out.print(errorResponse.toString());
            out.flush();
            return;
        }
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        JSONObject jsonObject = new JSONObject(sb.toString());
        String userKey = jsonObject.getString("Authorization"), actualKey;

        

        if (userKey != null && userKey.startsWith("Bearer ")) {
            actualKey = userKey.substring(7);  // remove "Bearer " part
        } else {
            actualKey = userKey;  // fallback if it's just a raw key
        }

        boolean isValidKey = authentication.AuthToken(actualKey);

        if(!isValidKey){
          PrintWriter out = Response.getWriter();
          
          JSONObject errorResponse = new JSONObject();
          errorResponse.put("error", "Unauthorized");

          Response.setContentType("application/json");
          Response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
          out.flush();
          return;
        }




        String jsonQuery = jsonObject.toString();
        HttpRequest request = HttpRequest.newBuilder()
          .uri(URI.create("https://hackrx-llm.onrender.com/process"))      
          .header("Content-Type", "application/json")
          .POST(HttpRequest.BodyPublishers.ofString(jsonQuery)) 
          .build();
        
        HttpResponse<String> httpResponse = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Response Code: " + httpResponse.statusCode());
       // System.out.println("Response Body: " + httpResponse.body());

        PrintWriter out = Response.getWriter();
        Response.setContentType("text/html");
        out.println("<h1>Response from HackRx</h1>");
        out.println("<pre>" + httpResponse.body() + "</pre>");
        
        Response.setContentType("application/json");
        out.print(httpResponse.body());
        out.flush();
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
