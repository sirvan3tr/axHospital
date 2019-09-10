import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Random;

public class Main {
  public static void main(String[] args) throws Exception {
    Random randomGenerator = SecureRandom.getInstance("SHA1PRNG");
    BigInteger randomInteger = new BigInteger(1024, randomGenerator);
    System.out.println(randomInteger);
  }
}