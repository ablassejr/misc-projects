package com.jpmc.midascore.component;

import org.springframework.beans.factory.annotation.Value;
import com.jpmc.midascore.foundation.Transaction;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class TransactionListener {
  public final String topic;
  public final KafkaTemplate<String, String> kafkaTemplate;

  public TransactionListener(@Value("${general.kafka-topic}") String topic, KafkaTemplate<String, String> kafkaTemplate) {
    this.topic = topic;
    this.kafkaTemplate = kafkaTemplate;
  }

  @KafkaListener(id = "transaction-listener", topics = "transactions")
  public void listen(Transaction sentTransaction) {
    System.out.println(sentTransaction.toString());
  }
}
