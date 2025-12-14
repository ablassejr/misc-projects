package barber;

public class Customer {
  private Thread thread;
  private int id;

  Customer(int id, Shop shop) {
    this.id = id;
    IO.println("Customer " + id + " enters the shop.");
    thread = new Thread(() -> shop.checkIn(this));
    thread.start();
  }

  public int getId() {
    return id;
  }

  public Thread getThread() {
    return thread;
  }
}
