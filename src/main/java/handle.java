import java.io.IOException; 
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/login")
public class handle extends HttpServlet {
  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException{
    response.setContentType("text/html");
    PrintWriter out = response.getWriter();
    out.println("<h1>Bad Request</h1>");
    
    out.close();
  }
  
  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    response.setContentType("text/html");
    PrintWriter out = response.getWriter();
    
    String textInput = request.getParameter("textInput");
    
    if (textInput != null && !textInput.isEmpty()) {
      out.println("<h1>Received Input: " + textInput + "</h1>");
    } else {
      out.println("<h1>No input received</h1>");
    }
    
    out.close();
  }
}
