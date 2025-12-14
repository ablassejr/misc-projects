package barber;

import java.util.concurrent.ThreadLocalRandom;
import java.util.LinkedList;
import java.util.Queue;

public class Shop {
  private static final int waitingChairs = 3;
  private static int occupiedChairs = 0;
  private static final Queue<Customer> waitQueue = new LinkedList<>();
  private static Shop instance = null;
  private static Barber barber;
  private static final Object lock = new Object();

  private Shop() {
    barber = Barber.getInstance(lock);
    barber.getThread().start();
    customerGen.start();
  }

  Runnable generateCustomers = () -> {
    int id = 0;
    while (id <= 15) {
      new Customer(id, this);
      long delay = ThreadLocalRandom.current().nextLong(1, 2000);
      id++;
      try {
        Thread.sleep(delay);
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        break;
      }
    }
  };
  Thread customerGen = new Thread(generateCustomers);

  public static Shop getInstance() {
    if (instance == null) {
      instance = new Shop();
    }
    return instance;
  }

  public void checkIn(Customer customer) {
    synchronized (lock) {
      if (occupiedChairs < waitingChairs) {
        waitQueue.add(customer);
        occupiedChairs++;
        IO.println("Customer " + customer.getId() + " is waiting. Available chairs: " + getAvailableChairs());
        lock.notify();
      } else {
        IO.println("No available chairs. Customer " + customer.getId() + " leaves.");
      }
    }
  }

  public static int getAvailableChairs() {
    synchronized (lock) {
      return waitingChairs - occupiedChairs;
    }
  }

  public static Customer getNextCustomer() {
    synchronized (lock) {
      while (waitQueue.isEmpty()) {
        IO.println("Barber goes to sleep.");
        try {
          lock.wait();
        } catch (InterruptedException e) {
          return null;
        }
      }
      occupiedChairs--;
      return waitQueue.poll();
    }
  }

  public static Object getLock() {
    return lock;
  }
}
