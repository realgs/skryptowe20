import scala.io.StdIn._

object StarczyJeden {
  val SEP = "\t"

  def main(args: Array[String]): Unit = {
    val argv = args.tail.toList

    readInput.filter(elem => existsInString(elem, argv)).foreach(println)
  }

  def readInput() : List[String] = {
    val line = readLine()
    line match {
      case null => Nil
      case str => str :: readInput
    }
  }

  def existsInString(str: String, list: List[String]): Boolean = {
    list.filter(elem => str.contains(elem)).nonEmpty
  }
}
