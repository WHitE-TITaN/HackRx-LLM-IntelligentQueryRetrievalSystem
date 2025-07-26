import java.io.IOException;
import java.io.PrintWriter;

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
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
    {
      PrintWriter out = response.getWriter();
      RequestDispatcher dispatch = request.getRequestDispatcher("error.jsp");
      response.setContentType("text/html");

      out.println("<h1>py Processing</h1>");
      dispatch.include(request, response);
    }
}
