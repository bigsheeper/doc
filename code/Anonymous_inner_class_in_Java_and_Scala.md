###In Java
```
public class Person {
    String getName() {
        return null;
    }

    public static void main(String[] args) {
        Person person = new Person() {
            @Override
            String getName() {
                return new String("big_sheep");
            }

            int getAge() {
                return 20;
            }
        };

// illegal
//        System.out.println("Name: " + person.getName() + "with age " + person.getAge());

// legal
        System.out.println("Age: " + new Person() {
            int getAge() {
                return 20;
            }
        }.getAge());

// legal
        Person person2 = new Person() {
            @Override
            String getName() {
                return new String("big_sheep with age " + getAge());
            }

            int getAge() {
                return 20;
            }
        };
        System.out.println("Name and Age: " + person2.getName());
    }
}
```

###In Scala
```
object Test {

  class Person {
    def getName(): String = {
      null
    }
  }

  def main(args: Array[String]) = {
    val person = new Person() {
      override def getName(): String = {
        "big_sheep"
      }

      def getAge(): Int = {
        20
      }
    }

// legal
    println("Name: " + person.getName() + " with age " + person.getAge())

// legal
    println("Age: " + new Person() {
      def getAge(): Int = {
        20
      }
    }.getAge())

// legal
    val person2 = new Person() {
      override def getName(): String = {
        "big_sheep with age " + getAge()
      }

      def getAge(): Int = {
        20
      }
    }
    System.out.println("Name and Age: " + person2.getName())
  }
  
}
```