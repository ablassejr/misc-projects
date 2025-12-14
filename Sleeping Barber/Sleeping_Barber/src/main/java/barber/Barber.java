package barber;

public class Barber {
  private static Barber instance = null;
  private static final int cutSpeed = 2000;
  private Thread thread;
  private Object lock;

  private Barber(Object lock) {
    this.lock = lock;
    IO.println("Barber has entered the shop.");
    thread = new Thread(() -> {
      while (!Thread.currentThread().isInterrupted()) {
        Customer customer = Shop.getNextCustomer();
        if (customer == null)
          break;
        IO.println("Barber is waking up.");
        IO.println("Barber is cutting Customer " + customer.getId() + "'s hair. Available chairs: "
            + Shop.getAvailableChairs());
        try {
          Thread.sleep(cutSpeed);
        } catch (InterruptedException e) {
          break;
        }
        IO.println("Barber has finished cutting hair of Customer " + customer.getId() + ".");
      }
    });
  }

  public static Barber getInstance(Object lock) {
    if (instance == null) {
      instance = new Barber(lock);
    }
    return instance;
  }

  public Thread getThread() {
    return thread;
  }
}
