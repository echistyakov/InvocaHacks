import scala.io.Source
import breeze.linalg._
import breeze.plot._

object HelloWorld{
  def main(args: Array[String]) {


     //time_vs_rating("sample.txt")
   }

   def time_vs_rating(filename: String){
     for (line <- Source.fromFile(filename).getLines()) {
       val split_string = line.split(" ")
       val time = split_string(0)
       val rating = split_string(1)

       println("time = " + time)
       println("rating = " + rating)
     }

     val f = Figure()
     val p = f.subplot(0)
     val x = linspace(0.0,10.0)
     p += plot(x, x :^ 2.0)
     p += plot(x, x :^ 3.0, '.')


     p.xlabel = "Time"
     p.ylabel = "y axis"
     f.saveas("lines.png")

   }
}
