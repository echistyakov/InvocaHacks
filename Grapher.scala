import scala.io.Source
import scalax.chart.api._

object HelloWorld {
  def main(args: Array[String]) {
    val ret = read_data_into_list("test.txt")

    val positivity_func = (list: List[(Double,Double,Double,Double,Double)]) => {
      list.map( x => (x._1, x._3))
    }

    plot_xy_graph(ret, positivity_func, "positivityIndex.png")

  }

  def plot_xy_graph(data: List[(Double,Double,Double,Double,Double)],
    xy_convert: List[(Double,Double,Double,Double,Double)] => List[(Double,Double)],
    name: String) =
  {
    val xy_pairs = xy_convert(data)
    val chart = XYLineChart(xy_pairs)
    chart.saveAsPNG("./" + name)
  }


  def read_data_into_list(filename: String): List[(Double,Double,Double,Double,Double)] = {
    var a : List[(Double,Double,Double,Double,Double)] = List()
    for (line <- Source.fromFile(filename).getLines()) {
      // minutes-rate-conf-conf-conf
      val split_string = line.split(" ")

      val minutes = split_string(0).toDouble
      val review = split_string(1).toDouble
      val pos_conf = split_string(2).toDouble
      val neu_conf = split_string(3).toDouble
      val neg_conf = split_string(4).toDouble

      a = a:+(minutes, review, pos_conf, neu_conf, neg_conf)
    }
    return a
  }

  def print_double_tuple_arr(list: List[(Double, Double, Double, Double, Double)]) = {
    list.foreach( a => { println("(" + a._1 + ", " + a._2 + ")") } )
  }
}
