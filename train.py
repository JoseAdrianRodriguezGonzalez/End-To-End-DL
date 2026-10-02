def main() -> None:
    batch_size = 64
    learning_rate = 0.2

    model, history, test, criterion, device = train_model(
        batch_size=batch_size,
        learning_rate=learning_rate
    )

    torch.save(
        model.state_dict(),
        "artifacts/best_model.pth"
    )

    test_loss = evaluate(
        model,
        test,
        criterion,
        device
    )

    print(f"Test loss {test_loss}")

    plot_history(history)


if __name__ == "__main__":
    main()
