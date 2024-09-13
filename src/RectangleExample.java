public class RectangleExample {

    public static void main(String[] args) {
        System.out.println("Creating a rectangle with side lengths 40 and 50");
        Rectangle rectangle = new Rectangle();
        rectangle.setWidth(40);
        rectangle.setHeight(50);

        System.out.println("The area of the rectangle is " + rectangle.area());
        System.out.println("(The correct area is 2000)\n");

        System.out.println("The diagonal length of the rectangle is " + rectangle.diagonalLength());
        System.out.println("(The correct diagonal length is approximately 64.03)\n");

        System.out.println("Is the rectangle a square? " + rectangle.isSquare());
        System.out.println("(The correct answer should be false)\n");

        System.out.println("------------------------------------------------");
        System.out.println("Creating a square with side lenth 20");
        Rectangle square = new Rectangle();
        square.setWidth(20);
        square.setHeight(20);

        System.out.println("The area of the square is " + square.area());
        System.out.println("(The correct area is 400)\n");

        System.out.println("The diagonal length of the square is " + square.diagonalLength());
        System.out.println("(The correct diagonal length is approximately 28.28)\n");

        System.out.println("Is the square a square? " + square.isSquare());
        System.out.println("(The correct answer should be true)\n");
    }

}
